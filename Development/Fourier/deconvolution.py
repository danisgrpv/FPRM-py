import numpy as np

def get_complex_spectrum(interf):
    """
    Возвращает комплексный Фурье-спектр интерференционной
    картины исследуемого изображения

    Параметры:
        1. interf : array_like, shape (n, m)
            Интерференционная картина исследуемого объекта
            n, m - количество пикселей изображения по каждой
            из координатных осей

    Возвращаемые значения:
        1. complex_spectrum :  array_like, shape (n, m)
            Комплексный Фурье-спектр
    """

    # Прямое Фурье-преобразование
    complex_spectrum = np.fft.fft2(interf)
    # Сдвиг спектра (нулевая частота смещается в центр)
    complex_spectrum = np.fft.fftshift(complex_spectrum)
    return complex_spectrum


def get_amplitude(complex_spectrum):
    """
    Возвращает амплитуду комплексного Фурье-спектра
    исследуемого изображения

    Параметры:
        1. complex_spectrum : array_like, shape (n, m)
            Комплексный Фурье-спектр исследуемого
            изображения

        2. amplitude : array_like, shape (n, m)
            Амплитуда комплексного спектра
            (на фазовой плоскости)
    """

    amplitude = np.abs(complex_spectrum)**(1/3)
    return amplitude


def get_complex_spectrum_part(amplitude, complex_spectrum, x0=0, y0=0, r=25):
    """
    """
    n, m = amplitude.shape
    pad = r
    cutted_complex_spectrum = np.zeros_like(complex_spectrum[x0-pad:x0+pad, y0-pad:y0+pad], dtype=complex)
    cutted_complex_spectrum = complex_spectrum[x0-pad:x0+pad, y0-pad:y0+pad]
    cutted_complex_spectrum = np.pad(cutted_complex_spectrum, n//2-pad, constant_values=(0+0j))
    return cutted_complex_spectrum


def get_phase(complex_spectrum):
    """
    Возращает фазовое распределение исследуемого объекта

    Параметры:
        1. complex_spectrum :  array_like, shape (n, m)
            Комплексный Фурье-спектр
    
    Возвращаемые значения:
        1. phase_unwraped : array_like, shape (n, m)
            Фазовое распределение исследуемого объекта
    """
    complex_spectrum = np.fft.ifftshift(complex_spectrum)
    wave_front = np.fft.ifft2(complex_spectrum)
    # Cвернутая фаза (фазовая развертка)
    phase = np.angle(wave_front)
    phase_ = phase - np.min(phase)
    # Развёртка фазы
    phase_unwraped = np.unwrap(phase_, axis=0)
    return phase_unwraped


def get_opd(phase_unwraped, lambda0):
    OPD = phase_unwraped * lambda0 / (2 * np.pi)
    OPD = OPD - np.min(OPD)
    return OPD