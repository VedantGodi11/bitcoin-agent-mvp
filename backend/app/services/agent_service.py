from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
import re
from bitcoinlib.scripts import Script

class AgentService:
    @staticmethod
    def process_message(message: str) -> str:
        """
        Process user message and return agent response.
        Enhanced with Bitcoin script generation capabilities.
        """
        message_lower = message.lower()
        wants_validate = "validate" in message_lower
        wants_generate = any(word in message_lower for word in ["script", "create", "generate", "make"])

        # Check for specific script explanations first
        if "p2pkh" in message_lower and ("explain" in message_lower or "what" in message_lower):
            return AgentService._explain_p2pkh()

        if ("multisig" in message_lower or "multi-sig" in message_lower) and ("explain" in message_lower or "what" in message_lower):
            return AgentService._explain_multisig()

        if "timelock" in message_lower and ("explain" in message_lower or "what" in message_lower):
            return AgentService._explain_timelock()

        # Handle combined validation and generation
        if wants_validate and wants_generate:
            validation_result = AgentService._validate_bitcoin_script(message)
            generated_script = AgentService._generate_bitcoin_script(message)
            return f"{validation_result}\n\n---\n\n{generated_script}"

        # Then check for script generation
        if wants_generate:
            return AgentService._generate_bitcoin_script(message)

        # Then check for validation
        if wants_validate:
            return AgentService._validate_bitcoin_script(message)

        # Generic explain response
        if "explain" in message_lower:
            return "I can explain Bitcoin scripts in plain English. Try asking 'explain P2PKH', 'explain multisig', or 'explain timelock'."

        # Default response
        return "I'm here to help with Bitcoin smart contracts. I can generate scripts, validate them, or explain how they work. Try asking me to 'create a P2PKH script' or 'explain multisig'!"

    @staticmethod
    def _generate_bitcoin_script(message: str) -> str:
        """Generate a Bitcoin script based on user request"""
        message_lower = message.lower()

        if "p2pkh" in message_lower:
            return """Here's a basic Pay-to-Public-Key-Hash (P2PKH) script:

**Locking Script (on the output):**
```
OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
```

**Unlocking Script (in the input):**
```
<signature> <pubkey>
```

This script ensures that only the owner of the private key corresponding to the public key hash can spend the coins.

Would you like me to explain how this works or create a different type of script?"""

        elif "multisig" in message_lower or "multi-sig" in message_lower:
            return """Here's a 2-of-3 multisignature script:

**Locking Script:**
```
2 <pubkey1> <pubkey2> <pubkey3> 3 OP_CHECKMULTISIG
```

**Unlocking Script:**
```
OP_0 <signature1> <signature2>
```

This requires 2 out of 3 signatures to spend the coins, providing security through multiple keys.

Would you like me to generate a script with different signature requirements?"""

        elif "timelock" in message_lower:
            return """Here's a time-locked script using CHECKLOCKTIMEVERIFY:

**Locking Script:**
```
<pubkey> OP_CHECKSIGVERIFY <locktime> OP_CHECKLOCKTIMEVERIFY
```

**Unlocking Script:**
```
<signature>
```

This script can only be spent after the specified locktime (block height or timestamp).

Would you like me to create a script with a specific locktime?"""

        else:
            return """I can generate several types of Bitcoin scripts:

1. **P2PKH** - Pay to Public Key Hash (standard address)
2. **Multisig** - Multiple signature requirements
3. **Timelock** - Time-based spending restrictions

Try asking for "create a P2PKH script" or "generate multisig script"!

What type of script would you like me to create?"""

    @staticmethod
    def _explain_p2pkh() -> str:
        return """**Pay-to-Public-Key-Hash (P2PKH) Explanation:**

P2PKH is the most common Bitcoin script type. Here's how it works:

1. **Locking coins:** The sender creates an output with the recipient's public key hash
2. **Spending coins:** The recipient provides their public key and signature
3. **Verification:** The network checks that:
   - The signature is valid for the provided public key
   - The hash of the public key matches the hash in the locking script

**Security benefits:**
- Public key hash hides the actual public key until spending
- Prevents quantum computing attacks on known public keys
- Standard for most Bitcoin transactions"""

    @staticmethod
    def _explain_multisig() -> str:
        return """**Multisignature (Multisig) Explanation:**

Multisig allows multiple parties to control coins together. For example, "2-of-3" means:

- 3 public keys are stored in the script
- At least 2 valid signatures are required to spend
- Provides security through distributed control

**Use cases:**
- Business accounts (CEO + CFO approval)
- Inheritance (family members as co-signers)
- Escrow services (buyer + seller + mediator)

**Script structure:**
```
M <pubkey1> <pubkey2> ... <pubkeyN> N OP_CHECKMULTISIG
```
Where M is minimum signatures required, N is total keys."""

    @staticmethod
    def _explain_timelock() -> str:
        return """**Timelock Explanation:**

Timelocks restrict when coins can be spent using CHECKLOCKTIMEVERIFY (CLTV):

**How it works:**
- Locktime can be a block height or Unix timestamp
- Coins cannot be spent until the blockchain reaches that point
- Useful for escrow, inheritance, and complex contracts

**Example script:**
```
<pubkey> OP_CHECKSIGVERIFY <locktime> OP_CHECKLOCKTIMEVERIFY
```

**Use cases:**
- **Escrow:** Funds locked until dispute resolution
- **Inheritance:** Automatic distribution after time period
- **Savings:** Prevent impulsive spending

The locktime is specified in the transaction's nLockTime field."""

    @staticmethod
    def _validate_bitcoin_script(message: str) -> str:
        """Validate a Bitcoin script and provide analysis"""
        # Try to extract script from the message
        script_patterns = [
            r'OP_DUP\s+OP_HASH160\s+.*?\s+OP_EQUALVERIFY\s+OP_CHECKSIG',  # P2PKH
            r'\d+\s+.*?\s+\d+\s+OP_CHECKMULTISIG',  # Multisig
            r'.*?OP_CHECKLOCKTIMEVERIFY',  # Timelock
            r'OP_\w+',  # Any OP codes
        ]

        message_lower = message.lower()

        # Check if message contains a script
        script_found = False
        for pattern in script_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                script_found = True
                break

        if not script_found:
            return """I can validate Bitcoin scripts! Please provide a script to validate. Here are some examples:

**P2PKH Script:**
```
OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
```

**Multisig Script:**
```
2 <pubkey1> <pubkey2> <pubkey3> 3 OP_CHECKMULTISIG
```

**Timelock Script:**
```
<pubkey> OP_CHECKSIGVERIFY <locktime> OP_CHECKLOCKTIMEVERIFY
```

Just paste your script and I'll analyze it!"""

        # Try to parse and validate the script
        try:
            # Extract script content (basic extraction)
            script_text = message.strip()

            # Remove markdown code blocks if present
            script_text = re.sub(r'```\w*\n?', '', script_text)
            script_text = re.sub(r'```', '', script_text)

            # Basic validation using bitcoinlib
            script = Script(script_text)

            # Analyze the script
            analysis = AgentService._analyze_script(script_text)

            return f"""**Script Validation Result:**

✅ **Script is syntactically valid**

**Analysis:**
{analysis}

**Script Details:**
- Length: {len(script_text.split())} opcodes
- Type: {AgentService._identify_script_type(script_text)}

**Note:** This is a basic validation. For production use, always test scripts on testnet first!"""

        except Exception as e:
            return f"""**Script Validation Failed**

❌ **Invalid Script**

**Error:** {str(e)}

**Common Issues:**
- Invalid opcode names
- Incorrect parameter order
- Missing required opcodes
- Syntax errors

Please check your script syntax and try again. You can ask me to generate example scripts if needed."""

    @staticmethod
    def _analyze_script(script_text: str) -> str:
        """Analyze a Bitcoin script and provide details"""
        analysis = []

        # Check for P2PKH pattern
        if re.search(r'OP_DUP.*OP_HASH160.*OP_EQUALVERIFY.*OP_CHECKSIG', script_text, re.IGNORECASE):
            analysis.append("• Standard P2PKH (Pay-to-Public-Key-Hash) pattern detected")
            analysis.append("• Requires signature + public key to spend")
            analysis.append("• Most common Bitcoin address type")

        # Check for multisig pattern
        multisig_match = re.search(r'(\d+)\s+.*?(\d+)\s+OP_CHECKMULTISIG', script_text, re.IGNORECASE)
        if multisig_match:
            m, n = multisig_match.groups()
            analysis.append(f"• Multisignature script: {m}-of-{n}")
            analysis.append(f"• Requires {m} out of {n} signatures to spend")
            analysis.append("• Provides distributed control and security")

        # Check for timelock
        if 'OP_CHECKLOCKTIMEVERIFY' in script_text.upper():
            analysis.append("• Contains timelock (OP_CHECKLOCKTIMEVERIFY)")
            analysis.append("• Funds cannot be spent until specified time/block height")
            analysis.append("• Useful for escrow, inheritance, savings")

        if 'OP_CHECKSEQUENCEVERIFY' in script_text.upper():
            analysis.append("• Contains relative timelock (OP_CHECKSEQUENCEVERIFY)")
            analysis.append("• Enforces relative time delays")

        # Check for hash locks
        if 'OP_HASH160' in script_text.upper() or 'OP_SHA256' in script_text.upper():
            analysis.append("• Contains hash-based conditions")
            analysis.append("• May require preimage or hash revelation to spend")

        if not analysis:
            analysis.append("• Custom script structure")
            analysis.append("• Manual review recommended")

        return "\n".join(analysis)

    @staticmethod
    def _identify_script_type(script_text: str) -> str:
        """Identify the type of Bitcoin script"""
        if re.search(r'OP_DUP.*OP_HASH160.*OP_EQUALVERIFY.*OP_CHECKSIG', script_text, re.IGNORECASE):
            return "P2PKH (Pay-to-Public-Key-Hash)"
        elif re.search(r'OP_CHECKMULTISIG', script_text, re.IGNORECASE):
            return "Multisignature"
        elif 'OP_CHECKLOCKTIMEVERIFY' in script_text.upper():
            return "Timelock (CLTV)"
        elif 'OP_CHECKSEQUENCEVERIFY' in script_text.upper():
            return "Relative Timelock (CSV)"
        else:
            return "Custom Script"

    @staticmethod
    def save_message(db: Session, session_id: int, role: str, content: str) -> models.Message:
        """Save a message to the database"""
        db_message = models.Message(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get_conversation_history(db: Session, session_id: int) -> List[models.Message]:
        """Get conversation history for a session"""
        return db.query(models.Message).filter(
            models.Message.session_id == session_id
        ).order_by(models.Message.created_at).all()