import numpy as np
import cv2

class LaplacianUtils:
    @staticmethod
    def compute_laplacian_variance(gray: np.ndarray) -> float:
        """
        Computes the variance of the Laplacian of a grayscale image, indicating image sharpness or blur.
        Args:
            gray: Grayscale image array.
        Returns:
            Variance of the Laplacian.
        """
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return float(laplacian.var())

    def compute_mean_gradient(gray: np.ndarray, ksize: int = 3) -> float:
        """
        Computes the mean gradient magnitude of a grayscale image.
        Args:
            gray: Grayscale image array.
            ksize: Sobel kernel size.
        Returns:
            Mean gradient magnitude.
        """
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        return float(np.mean(magnitude))

    @staticmethod
    def compute_edge_density(gray: np.ndarray, lower_factor: float = 0.67, upper_factor: float = 1.33) -> float:
        """
        Computes the edge density of a grayscale image using the Canny edge detector.
        Args:
            gray: Grayscale image array.
            lower_factor: Factor for lower threshold.
            upper_factor: Factor for upper threshold.
        Returns:
            Ratio of edge pixels to total pixels.
        """
        median_val = np.median(gray)
        lower = int(max(0, lower_factor * median_val))
        upper = int(min(255, upper_factor * median_val))
        edges = cv2.Canny(gray, lower, upper)
        total_pixels = gray.shape[0] * gray.shape[1]
        edge_pixels = np.sum(edges > 0)
        return float(edge_pixels / total_pixels)

    @staticmethod
    def compute_local_variance_consistency(gray: np.ndarray, block_size: int) -> float:
        """
        Computes the standard deviation of Laplacian variances across local blocks in a grayscale image.
        Args:
            gray: Grayscale image array.
            block_size: Size of the local block.
        Returns:
            Standard deviation of local Laplacian variances.
        """
        rows, cols = gray.shape
        block_variances = []
        for r in range(0, rows - block_size + 1, block_size):
            for c in range(0, cols - block_size + 1, block_size):
                block = gray[r : r + block_size, c : c + block_size]
                lap = cv2.Laplacian(block, cv2.CV_64F)
                block_variances.append(lap.var())
        if not block_variances:
            return 0.0
        return float(np.std(block_variances))
