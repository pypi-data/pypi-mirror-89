class EncryptedMessageError(Exception):
    """Encrypted message could not be opened."""
    pass


class NoSenderKeyFoundError(Exception):
    """Sender private key was not available to sign a payload message."""
    pass


class NoSuitableProtocolFoundError(Exception):
    """No suitable protocol found to pass this payload message to."""
    pass


class SignatureVerificationError(Exception):
    """Authenticity of the signature could not be verified given the key."""
    pass
