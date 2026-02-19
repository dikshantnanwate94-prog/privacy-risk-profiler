import requests

class BreachChecker:
    BASE_URL = 'https://haveibeenpwned.com/api/v3/'

    def __init__(self):
        pass

    def check_email_breaches(self, email):
        """Check if an email has been compromised in data breaches."""
        response = requests.get(f'{self.BASE_URL}breachedaccount/{email}', headers={'User-Agent': 'BreachChecker'})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []  # No breaches found
        else:
            response.raise_for_status()

    def check_password_strength(self, password):
        """Check if a password has been exposed in data breaches."""
        hash_password = self._hash_password(password)
        response = requests.get(f'{self.BASE_URL}pwnedpasswords/range/{hash_password[:5]}')
        if response.status_code == 200:
            return self._parse_password_response(response.text, hash_password)
        else:
            response.raise_for_status()

    def get_breach_details(self, breach_name):
        """Get details about a specific breach."""
        response = requests.get(f'{self.BASE_URL}breaches/{breach_name}', headers={'User-Agent': 'BreachChecker'})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def _hash_password(self, password):
        """Hash the password using SHA-1."""
        import hashlib
        return hashlib.sha1(password.encode('utf-8')).hexdigest()

    def _parse_password_response(self, response, hash_password):
        """Parse password response to check exposure count."""
        for line in response.splitlines():
            parts = line.split(':')
            if parts[0].lower() == hash_password[5:]:
                return int(parts[1])  # Return the count of exposures
        return 0  # No exposure found
