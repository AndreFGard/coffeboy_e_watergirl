class Utils:
    def sum_vectors(v1:tuple, v2:tuple) -> tuple:
        """Sums the corresponding indexes of the vectors"""
        if len(v1) == 2:
            return v1[0] + v2[0], v1[1] + v2[2]