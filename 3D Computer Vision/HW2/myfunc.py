# reference
# https://github.com/opencv/opencv/blob/master/modules/calib3d/src/p3p.cpp
import math
import numpy as np
from scipy.spatial.transform import Rotation as Rot


class P3P(object):
    def __init__(self, camera_matrix, distCoeffs):
        self.camera_matrix = camera_matrix
        self.distCoeffs = distCoeffs

        self.focal_length_x = camera_matrix[0, 0]
        self.focal_length_y = camera_matrix[1, 1]
        self.center_x = camera_matrix[0, 2]
        self.center_y = camera_matrix[1, 2]

        self.inverse_focal_length_x = 1 / self.focal_length_x
        self.inverse_focal_length_y = 1 / self.focal_length_y
        self.cx_fx = self.center_x / self.focal_length_x
        self.cy_fy = self.center_y / self.focal_length_y


    def undistortion(self, points2D):
        points2D_reshape = np.insert(points2D, 2, np.ones(points2D.shape[0]), axis=1)
        return np.dot(np.linalg.inv(self.camera_matrix), points2D_reshape.T).T[:, :2]
    

    def solve_p3p(self, points2D, points3D):
        # Get the undistortetd 2D points
        undistorted_points2D = self.undistortion(points2D)
        undistorted_points_extract = undistorted_points2D[:3] 
        undistorted_points_extract = np.insert(undistorted_points_extract, 2, np.ones(len(undistorted_points_extract)), axis=1)
        
        # Calculate the 3D points distances
        distances = np.zeros(3, dtype=float)
        x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3 = points3D.flatten()
        points3D_roll = np.roll(points3D[:3, :], 1, axis=0)
        distances = np.roll(np.sqrt(np.power((points3D[:3,:] - points3D_roll), 2).sum(axis=1)), 1)

        # Calculate the 2D points distances
        mu0, mv0, mk0, mu1, mv1, mk1, mu2, mv2, mk2 = undistorted_points_extract.flatten()
        d0, d1, d2 = np.sqrt(np.power(undistorted_points_extract, 2).sum(axis=1))

        cosines = np.array([
            (mu1 * mu2 + mv1 * mv2 + mk1 * mk2) / (d1 * d2),
            (mu0 * mu2 + mv0 * mv2 + mk0 * mk2) / (d0 * d2),
            (mu0 * mu1 + mv0 * mv1 + mk0 * mk1) / (d0 * d1)
                ])
        
        possible_lengths = self.solve_distance_constraint(distances, cosines)

        # No usable solutions
        if len(possible_lengths) == 0:
            return 
        
        mu3, mv3 = undistorted_points2D[3]
        best_reprojection_error = 10e8
        best_Rs = None
        best_Ts = None
        for length in possible_lengths:
            M = np.tile(length, 3).reshape(3, 3).T * undistorted_points_extract
            R, T = self.solve_align_matrix(M, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            print(R,T)
            exit()
            reconstruct_points3D = np.dot(R, np.array([x3, y3, z3])) + T
            reconstruct_points3D = reconstruct_points3D / reconstruct_points3D[2]

            mu3p, mv3p = reconstruct_points3D[:2]
            
            error = np.sqrt((mu3p - mu3)**2 + (mv3p - mv3)**2)
            if error < best_reprojection_error:
                best_Rs = R
                best_Ts = T
                best_reprojection_error = error

        rotation_c = Rot.from_matrix(best_Rs)
        rvec = rotation_c.as_rotvec()

        return [rvec, best_Ts]
    

    def get_eigenvalues(self, Qs_matrix):
        indentity_matrix = np.eye(4, dtype=float).flatten()
        diagonals = [Qs_matrix[0], Qs_matrix[5], Qs_matrix[10], Qs_matrix[15]]
        eigenvalues = diagonals.copy()
        Z = [0,0,0,0]

        for iteration in range(50):
            summation = abs(Qs_matrix[1]) + abs(Qs_matrix[2]) + abs(Qs_matrix[3]) + abs(Qs_matrix[6]) + abs(Qs_matrix[7]) + abs(Qs_matrix[11])
            if summation == 0:
                return eigenvalues, indentity_matrix

            # increment the threshold
            threshold = (0.2 * summation / 16) if (iteration < 3) else 0

            for i in range(3):
                loc = 5*i + 1
                for j in range(i+1, 4):
                    Aij = Qs_matrix[loc]
                    epsilon = 100 * abs(Aij)
                    if (iteration > 3 and abs(eigenvalues[i]) + epsilon == abs(eigenvalues[i]) and abs(eigenvalues[j]) + epsilon == abs(eigenvalues[j])):
                        Qs_matrix[loc] = 0
                    elif abs(Aij) > threshold:
                        hh = eigenvalues[j] - eigenvalues[i]
                        if abs(hh) + epsilon == abs(hh):
                            t = Aij / hh
                        else:
                            theta = 0.5 * hh / Aij
                            t = 1 / (abs(theta) + math.sqrt(1 + theta * theta))
                            if (theta < 0):
                                t = -t

                        hh = t * Aij
                        Z[i] -= hh
                        Z[j] += hh
                        eigenvalues[i] -= hh
                        eigenvalues[j] += hh
                        Qs_matrix[loc] = 0

                        c = 1.0 / math.sqrt(1 + t * t)
                        s = t * c
                        tau = s / (1.0 + c)

                        for k in range(i):
                            g = Qs_matrix[k * 4 + i]
                            h = Qs_matrix[k * 4 + j]
                            Qs_matrix[k * 4 + i] = g - s * (h + g * tau)
                            Qs_matrix[k * 4 + j] = h + s * (g - h * tau)

                        for k in range(i+1, j):
                            g = Qs_matrix[i * 4 + k]
                            h = Qs_matrix[k * 4 + j]
                            Qs_matrix[i * 4 + k] = g - s * (h + g * tau)
                            Qs_matrix[k * 4 + j] = h + s * (g - h * tau)

                        for k in range(j+1, 4):
                            g = Qs_matrix[i * 4 + k]
                            h = Qs_matrix[j * 4 + k]
                            Qs_matrix[i * 4 + k] = g - s * (h + g * tau)
                            Qs_matrix[j * 4 + k] = h + s * (g - h * tau)

                        for k in range(4):
                            g = indentity_matrix[k * 4 + i]
                            h = indentity_matrix[k * 4 + j]
                            indentity_matrix[k * 4 + i] = g - s * (h + g * tau)
                            indentity_matrix[k * 4 + j] = h + s * (g - h * tau)

                    loc += 1
            for i in range(4):
                diagonals[i] += Z[i]
            eigenvalues = diagonals.copy()
            Z = [0,0,0,0]

        return eigenvalues, indentity_matrix

    def solve_align_matrix(self, M_end, X0, Y0, Z0, X1, Y1, Z1, X2, Y2, Z2):
        Rotation_matrix = np.zeros((3, 3), dtype=float)
        Translation_vector = np.zeros(3, dtype=float)

        # Centroids
        centroids = np.array([
            (X0 + X1 + X2) / 3,
            (Y0 + Y1 + Y2) / 3,
            (Z0 + Z1 + Z2) / 3
            ])
        centroids_end = M_end.mean(axis=0)

        covariance_matrix = np.zeros(9, dtype=float)
        for j in range(3):
            covariance_matrix[0 * 3 + j] = (X0 * M_end[0][j] + X1 * M_end[1][j] + X2 * M_end[2][j]) / 3 - centroids_end[j] * centroids[0]
            covariance_matrix[1 * 3 + j] = (Y0 * M_end[0][j] + Y1 * M_end[1][j] + Y2 * M_end[2][j]) / 3 - centroids_end[j] * centroids[1]
            covariance_matrix[2 * 3 + j] = (Z0 * M_end[0][j] + Z1 * M_end[1][j] + Z2 * M_end[2][j]) / 3 - centroids_end[j] * centroids[2]

        Qs = np.zeros(16, dtype=float)
        Qs[0 * 4 + 0] = covariance_matrix[0 * 3 + 0] + covariance_matrix[1 * 3 + 1] + covariance_matrix[2 * 3 + 2]
        Qs[1 * 4 + 1] = covariance_matrix[0 * 3 + 0] - covariance_matrix[1 * 3 + 1] - covariance_matrix[2 * 3 + 2]
        Qs[2 * 4 + 2] = covariance_matrix[1 * 3 + 1] - covariance_matrix[2 * 3 + 2] - covariance_matrix[0 * 3 + 0]
        Qs[3 * 4 + 3] = covariance_matrix[2 * 3 + 2] - covariance_matrix[0 * 3 + 0] - covariance_matrix[1 * 3 + 1]

        Qs[1 * 4 + 0] = Qs[0 * 4 + 1] = covariance_matrix[1 * 3 + 2] - covariance_matrix[2 * 3 + 1]
        Qs[2 * 4 + 0] = Qs[0 * 4 + 2] = covariance_matrix[2 * 3 + 0] - covariance_matrix[0 * 3 + 2]
        Qs[3 * 4 + 0] = Qs[0 * 4 + 3] = covariance_matrix[0 * 3 + 1] - covariance_matrix[1 * 3 + 0]
        Qs[2 * 4 + 1] = Qs[1 * 4 + 2] = covariance_matrix[1 * 3 + 0] + covariance_matrix[0 * 3 + 1]
        Qs[3 * 4 + 1] = Qs[1 * 4 + 3] = covariance_matrix[2 * 3 + 0] + covariance_matrix[0 * 3 + 2]
        Qs[3 * 4 + 2] = Qs[2 * 4 + 3] = covariance_matrix[2 * 3 + 1] + covariance_matrix[1 * 3 + 2]

        # Get the eigenvalues and keep the max
        evs, U = self.get_eigenvalues(Qs)
        ev_max = max(evs)
        i_ev = evs.index(ev_max)

        queternion_vector = np.array(U).reshape(4, 4)[:, i_ev]
        queternion_square = np.power(queternion_vector, 2)
        q0_1 = queternion_vector[0] * queternion_vector[1]
        q0_2 = queternion_vector[0] * queternion_vector[2]
        q0_3 = queternion_vector[0] * queternion_vector[3]
        q1_2 = queternion_vector[1] * queternion_vector[2]
        q1_3 = queternion_vector[1] * queternion_vector[3]
        q2_3 = queternion_vector[2] * queternion_vector[3]

        Rotation_matrix[0][0] = queternion_square[0] + queternion_square[1] - queternion_square[2] - queternion_square[3]
        Rotation_matrix[0][1] = 2. * (q1_2 - q0_3)
        Rotation_matrix[0][2] = 2. * (q1_3 + q0_2)

        Rotation_matrix[1][0] = 2. * (q1_2 + q0_3)
        Rotation_matrix[1][1] = queternion_square[0] + queternion_square[2] - queternion_square[1] - queternion_square[3]
        Rotation_matrix[1][2] = 2. * (q2_3 - q0_1)

        Rotation_matrix[2][0] = 2. * (q1_3 - q0_2)
        Rotation_matrix[2][1] = 2. * (q2_3 + q0_1)
        Rotation_matrix[2][2] = queternion_square[0] + queternion_square[3] - queternion_square[1] - queternion_square[2]

        for i in range(3):
            Translation_vector[i] = centroids_end[i] - (Rotation_matrix[i][0] * centroids[0] + Rotation_matrix[i][1] * centroids[1] + Rotation_matrix[i][2] * centroids[2])

        return Rotation_matrix, Translation_vector


    def solve_quartic_equation(self, parameters):
        out = []
        parameters = np.array(parameters, dtype=float)
        p = np.poly1d(parameters)
        r = np.roots(p)
        r = r[np.isreal(r)]
        for root in r:
            out.append(np.real(root))
        return out


    def solve_distance_constraint(self, distances, cosines):   
        p, q, r = cosines * 2
        d_square = distances ** 2
        a, b = (d_square / d_square[2])[:2]

        a_square = a ** 2
        b_square = b ** 2
        p_square = p ** 2
        q_square = q ** 2
        r_square = r ** 2
        pr = p * r
        pqr = pr * q

        if (p_square + q_square + r_square - pqr - 1 == 0):
            return []

        ab = a * b
        a_2 = 2 * a
        A = -2 * b + b_square + a_square + 1 + ab * (2 - r_square) - a_2

        if A == 0:
            return []

        a_4 = 4 * a
        B = q * (-2 * (ab + a_square + 1 - b) + r_square * ab + a_4) + pr * (b - b_square + ab)
        C = q_square + b_square * (r_square + p_square - 2) - b*(p_square + pqr) - ab * (r_square + pqr) + (a_square - a_2)*(2 + q_square) + 2
        D = pr * (ab - b_square + b) + q * ((p_square -2 ) * b + 2 * (ab - a_square) + a_4 - 2)
        E = 1 + 2 * (b - a - ab) + b_square - b * p_square + a_square

        temp = (p_square * (a-1+b) + r_square * (a-1-b) + pqr - a * pqr)
        b0 = b * temp * temp

        if b0 == 0:
            return []

        quartic_solutions = self.solve_quartic_equation([A, B, C, D, E])
        if len(quartic_solutions) == 0:
            return []

        r3 = r_square * r
        pr2 = p * r_square
        r3q = r3 * q
        inv_b0 = 1 / b0

        solution = []
        for x in quartic_solutions:
            if x <= 0:
                continue

            x2 = x**2
            b1 = ((1-a-b)*x2 + (q*a-q)*x + 1 - a + b) * (((r3*(a_square + ab*(2 - r_square) - a_2 + b_square - 2*b + 1)) * x + (r3q*(2*(b-a_square) + a_4 + ab*(r_square - 2) - 2) + pr2*(1 + a_square + 2*(ab-a-b) + r_square*(b - b_square) + b_square))) * x2 + (r3*(q_square*(1-2*a+a_square) + r_square*(b_square-ab) - a_4 + 2*(a_square - b_square) + 2) + r*p_square*(b_square + 2*(ab - b - a) + 1 + a_square) + pr2*q*(a_4 + 2*(b - ab - a_square) - 2 - r_square*b)) * x + 2*r3q*(a_2 - b - a_square + ab - 1) + pr2*(q_square - a_4 + 2*(a_square - b_square) + r_square*b + q_square*(a_square - a_2) + 2) + p_square*(p*(2*(ab - a - b) + a_square + b_square + 1) + 2*q*r*(b + a_2 - a_square - ab - 1)))

            if b1 <= 0:
                continue

            y = inv_b0 * b1
            v = x2 + y*y - x*y*r

            if v <= 0:
                continue

            Z = distances[2] / math.sqrt(v)
            X = x * Z
            Y = y * Z

            solution.append([X, Y, Z])

        return solution


def getUndistortedPoints(pixel_points, camera_matrix, distCoeffs):
    points2D_extend = np.insert(pixel_points, 2, np.ones(pixel_points.shape[0]), axis=1)
    result = np.dot(np.linalg.inv(camera_matrix), points2D_extend.T).T[:,:2]
    return result


def projection_error(points2D, points3D, R, T, cameraMatrix, distCoeffs):
    w_extend = np.insert(points3D, 3, np.ones(points3D.shape[0]), axis=1)
    undistorted_points = getUndistortedPoints(points2D, cameraMatrix, distCoeffs)
    RT = np.insert(R, 3, T, axis=1)
    css_p = np.dot(RT, w_extend.T).T
    css_p_rescale = (css_p.T / css_p[:,2]).T[:,:2]
    diff = undistorted_points - css_p_rescale
    diff_square_sum = np.power(diff, 2).sum()
    return diff_square_sum