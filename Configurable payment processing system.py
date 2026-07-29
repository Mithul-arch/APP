from abc import ABC, abstractmethod
import logging
# basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# 1. Strategy Interface
class PaymentStrategy(ABC):
    """Abstract base class for all payment strategies."""
    
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process the payment and return True if successful."""
        pass

# 2. Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, cardholder_name: str, card_number: str, cvv: str):
        self.cardholder_name = cardholder_name
        self.card_number = card_number
        self.cvv = cvv

    def process_payment(self, amount: float) -> bool:
        # In a real app, you would integrate with Stripe/Braintree here
        masked_card = f"****-****-****-{self.card_number[-4:]}"
        logging.info(f"[Credit Card] Charging ₹{amount:.2f} to {self.cardholder_name} ({masked_card})")
        return True

class PayPalPayment(PaymentStrategy):
    def __init__(self, email_address: str):
        self.email_address = email_address

    def process_payment(self, amount: float) -> bool:
        # In a real app,PayPal API will be hit here
        logging.info(f"[PayPal] Charging ${amount:.2f} to account: {self.email_address}")
        return True

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def process_payment(self, amount: float) -> bool:
        # In a real app,there will be a broadcast of transaction to the blockchain
        logging.info(f"[Crypto] Transferring ₹{amount:.2f} to wallet: {self.wallet_address}")
        return True

# 3. The Context
class PaymentProcessor:
    """The Context that uses the configured PaymentStrategy."""
    
    def __init__(self, strategy: PaymentStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        """Allows switching the payment strategy at runtime."""
        self._strategy = strategy
        logging.info(f"Switched payment method to {strategy.__class__.__name__}")

    def checkout(self, amount: float) -> None:
        """Executes the payment using the current strategy."""
        if not self._strategy:
            raise ValueError("Payment strategy is not set. Cannot process payment.")
        
        logging.info("Initiating checkout process...")
        
        success = self._strategy.process_payment(amount)
        
        if success:
            logging.info("Checkout complete! Payment was successful.\n")
        else:
            logging.error("Checkout failed! Payment was declined.\n")

# 4. Example
if __name__ == "__main__":
    # 1. Initialize the central processor
    processor = PaymentProcessor()
    # 2. Customer selects Credit Card
    cc_strategy = CreditCardPayment("Mithul Krishna", "1234567890124242", "123")
    processor.set_strategy(cc_strategy)
    processor.checkout(150.00)
    # 3. Customer switches to PayPal for their next purchase
    paypal_strategy = PayPalPayment("Mithul@example.com")
    processor.set_strategy(paypal_strategy)
    processor.checkout(45.50)
    # 4. Customer switches to Crypto
    crypto_strategy = CryptoPayment("0x71C7656EC7ab88b098defB751B7401B5f6d8976F")
    processor.set_strategy(crypto_strategy)
    processor.checkout(34772.94)
