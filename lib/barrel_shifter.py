class BarrelShifter:
    @classmethod
    def asr(self, val, n):
        return val >> n

    @classmethod
    def asl(self, val, n):
        return val << n

    @classmethod
    def lsr(cls, val, n):
        # VERIFY
        return (val % 0x100000000) >> n

    @classmethod
    def lsl(cls, val, n):
        # VERIFY
        return (val % 0x100000000) << n

    @classmethod
    def ror(cls, val, n=1):
        return int(f"{val:032b}"[-n:] + f"{val:032b}"[:-n], 2)

    @classmethod
    def reverse_bytes_word(cls, val, n=1):
        raise NotImplementedError()

    @classmethod
    def reverse_bytes_half_word(cls, val, n=1):
        raise NotImplementedError()

    @classmethod
    def reverse_bytes_half_word_signal(cls, val, n=1):
        raise NotImplementedError()
