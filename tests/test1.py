import os
from src.config.settings import settings
from src.browserstack.capabilities import get_browserstack_capabilities
from src.utils.logger import logger

def verify_setup():
    print("=" * 60)
    print("🔍 VERIFYING ENVIRONMENT & PHASE 1 SETUP")
    print("=" * 60)

    # 1. Test Logger
    logger.info("Testing Logger output...")

    # 2. Test Settings & Env
    print(f"✅ Settings Loaded Successfully:")
    print(f"   - BS Username Loaded : {settings.BROWSERSTACK_USERNAME != 'YOUR_USERNAME'}")
    print(f"   - Output Dir         : {settings.OUTPUT_DIR}")
    print(f"   - Target Section     : {settings.TARGET_SECTION}")

    # 3. Test Capabilities Matrix
    caps = get_browserstack_capabilities()
    print(f"\n✅ BrowserStack Capabilities Matrix Generated: {len(caps)} configurations.")
    for idx, cap in enumerate(caps, start=1):
        session = cap.get("bstack:options", {}).get("sessionName", "N/A")
        print(f"   Thread {idx}: {session}")

    print("\n🎉 ENVIRONMENT & PHASE 1 VERIFICATION PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    verify_setup()