import abc


class IAgentOTPProvider(metaclass=abc.ABCMeta):
    """
    IAgentOTPProvider provides an interface for other components to get one-time passwords (OTPs).
    Notably, this is used by exploiters during propagation to get OTPs for running new
    Agents on exploited machines, so that they can authenticate with the Island.
    """

    @abc.abstractmethod
    def get_otp(self) -> str:
        """
        Gets a one-time password (OTP)

        :return: An OTP
        """
        pass
