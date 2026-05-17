from typing import Dict, List

class BitcoinService:
    @staticmethod
    def validate_script(script_content: str) -> Dict:
        """
        Validate a Bitcoin script.
        For MVP, this is basic validation.
        In production, this would use bitcoinlib or similar.
        """
        errors = []
        warnings = []

        # Basic validation rules
        if not script_content or not script_content.strip():
            errors.append("Script content cannot be empty")
            return {"is_valid": False, "errors": errors, "warnings": warnings}

        script = script_content.strip()

        # Check for basic script structure
        if not script.startswith("OP_") and not any(op in script.upper() for op in ["DUP", "HASH160", "EQUALVERIFY", "CHECKSIG"]):
            warnings.append("Script may not be a valid Bitcoin script - missing common opcodes")

        # Check for balanced parentheses if present
        if "(" in script or ")" in script:
            open_count = script.count("(")
            close_count = script.count(")")
            if open_count != close_count:
                errors.append("Unbalanced parentheses in script")

        # Check for common security issues
        if "OP_RETURN" in script.upper():
            warnings.append("Script contains OP_RETURN - this makes outputs unspendable")

        # For MVP, assume valid if no errors
        is_valid = len(errors) == 0

        return {
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def generate_script(description: str) -> str:
        """
        Generate a Bitcoin script from description.
        For MVP, this returns a simple template.
        In production, this would use AI to generate actual scripts.
        """
        description_lower = description.lower()

        if "p2pkh" in description_lower or "pay to pubkey hash" in description_lower:
            return "OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG"

        if "multisig" in description_lower:
            return "OP_2 <pubKey1> <pubKey2> <pubKey3> OP_3 OP_CHECKMULTISIG"

        if "timelock" in description_lower:
            return "<timestamp> OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG"

        # Default simple script
        return "OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG"