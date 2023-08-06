"""Gerchberg-Saxton Error Reduction algorithm."""

from prysm.mathops import engine as np


class GerchbergSaxton:
    """Container for state of the GS algorithm."""

    def __init__(self, pupil_intensity, psf_intensity, pupil_phase=None):
        """Create a new GS instance.

        Parameters
        ----------
        pupil_intensity : `numpy.ndarray`
            intensity of the pupil plane
        psf_intensity : `numpy.ndarray`
            intensity of the psf plane
        pupil_phase : `numpy.ndarray`, optional
            initial estimate for the phase of the pupil, radians
            if None, zeros_like(pupil_intensity)

        """
        if pupil_phase is None:
            pupil_phase = np.zeros_like(pupil_intensity)
        self.pupil_intensity = pupil_intensity
        self.pupil_amp = np.sqrt(pupil_intensity)
        self.pupil_phase = pupil_phase
        self.psf_intensity = psf_intensity
        self.psf_amp = np.sqrt(psf_intensity)
        self.iters = 0
        self.err_hist = []

    def step(self, track_err=True):
        """Step the algorithm forward one iteration."""

        # compute the pupil from the current pupil phase
        # and known amplitude
        pupil = self.pupil_amp * np.exp(1j * self.pupil_phase)

        # propagate to get the field in the PSF plane
        psf = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(pupil)))

        if track_err:  # mean square error
            psf2 = abs(psf)**2
            err = (psf2 - self.psf_intensity)**2
            err /= err.size
            self.err_hist.append(err.sum())

        # combine the phase of the forward PSF with the known amplitude
        psf_phase = np.angle(psf)
        psf = self.psf_amp * np.exp(1j * psf_phase)

        # reverse transform and apply known amp, extract phase
        pupil = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(psf)))
        self.pupil_phase = np.angle(pupil)
        self.iters += 1
        return
