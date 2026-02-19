import requests
import hashlib

class BreachChecker:
    # Using XposedOrNot's free community API
    BASE_URL = 'https://api.xposedornot.com/v1/'
    PASS_URL = 'https://passwords.xposedornot.com/v1/pass/anon/'

    def check_email_breaches(self, email):
        """Check if an email has been compromised using XposedOrNot."""
        try:
            response = requests.get(f'{self.BASE_URL}check-email/{email}')
            if response.status_code == 200:
                # Returns a list of breach names under the 'breaches' key
                return response.json().get('breaches', [])
            elif response.status_code == 404:
                return []  # No breaches found
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Connection Error: {e}"

    def check_password_strength(self, password):
        """Check if a password has been exposed using k-anonymity (KECCAK-512)."""
        # XposedOrNot uses SHA3-keccak-512 for password anonymity
        from sha3 import keccak_512 # You may need to pip install pysha3
        
        hash_obj = keccak_512()
        hash_obj.update(password.encode('utf-8'))
        full_hash = hash_obj.hexdigest()
        
        # We only send the first 10 characters to the API (k-anonymity)
        prefix = full_hash[:10]
        
        try:
            response = requests.get(f'{self.PASS_URL}{prefix}')
            if response.status_code == 200:
                data = response.json()
                # If prefix matches, it returns the exposure count
                return data.get('SearchPassAnon', {}).get('count', 0)
            return 0
        except Exception as e:
            return f"Error: {e}"

# --- Example Usage ---
# checker = BreachChecker()
# print(checker.check_email_breaches("test@example.com"))
