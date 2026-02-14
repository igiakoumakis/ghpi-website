import streamlit as st
import os

# DEFINE THE TAGS
# These tell WhatsApp/Facebook what to show
meta_tags = """
<title>Greece House Price Index (GHPI)</title>
<meta property="og:title" content="Greece House Price Index (GHPI)" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://www.ghpi.gr/" />
<meta property="og:description" content="The official composite index tracking the Greek Real Estate Market. Detailed analytics and trends." />
<meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Greece.svg/1200px-Flag_of_Greece.svg.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Greece.svg/1200px-Flag_of_Greece.svg.png" />
"""

# LOCATE STREAMLIT INSTALLATION
# We find where Streamlit is installed inside the Railway server
pkg_path = os.path.dirname(st.__file__)
index_path = os.path.join(pkg_path, "static", "index.html")

# INJECT THE TAGS
print(f"Injecting tags into: {index_path}")

# Read the original file
with open(index_path, "r", encoding='utf-8') as f:
    html = f.read()

# Replace the <head> tag with our custom version
if "Greece House Price Index" not in html:
    new_html = html.replace("<head>", f"<head>{meta_tags}")
    
    # Save the modified file
    with open(index_path, "w", encoding='utf-8') as f:
        f.write(new_html)
    print("✅ Success! Meta tags injected.")
else:
    print("⚠️ Tags already present.")
