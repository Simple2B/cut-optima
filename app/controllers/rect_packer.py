from rectpack import newPacker, guillotine


class RectPacker:
    def __init__(self):
        self.packer = newPacker(pack_algo=guillotine.GuillotineBssfMaxas)
        self.bins = []
        self.rectangles = []

    def add_bin(self, width: float, height: float):
        self.bins.append([width, height])

    def add_rectangle(self, width: float, height: float):
        self.rectangles.append([width, height])

    def validate_rectangles(self):
        if not self.bins:
            raise ValueError("Bins not found")
        elif not self.rectangles:
            raise ValueError("Rectangles not found")
        invalid_rectangles = []

        for rect in self.rectangles:
            rect = sorted(rect)
            fit_in_bins = []
            for bin in self.bins:
                bin = sorted(bin)
                fit_in_bins.append(rect[0] < bin[0] and rect[1] < bin[0])
            if not any(fit_in_bins):
                invalid_rectangles.append(rect)

        if invalid_rectangles:
            raise ValueError(f"Found invalid rectangle(s): {invalid_rectangles}")
