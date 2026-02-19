class RiskCalculator:
    def __init__(self, user_data):
        self.user_data = user_data

    def calculate_privacy_score(self):
        # Implement privacy score calculation logic here
        score = 0
        # Example logic: More personal data can reduce score
        if self.user_data.get('sensitive_info'):
            score -= 10
        if self.user_data.get('sharing_with_third_parties'):
            score -= 5
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        return score

    def generate_recommendations(self):
        recommendations = []
        score = self.calculate_privacy_score()
        if score < 50:
            recommendations.append("Consider reducing the amount of personal data you share.")
            recommendations.append("Review your privacy settings on social media platforms.")
        else:
            recommendations.append("Your privacy score is sufficient.")
            recommendations.append("Continue monitoring your data sharing practices.")
        return recommendations

# Example usage:
# user_data = { 'sensitive_info': True, 'sharing_with_third_parties': False }
# risk_calculator = RiskCalculator(user_data)
# print(risk_calculator.calculate_privacy_score())
# print(risk_calculator.generate_recommendations())