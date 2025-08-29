import streamlit as st
import qrcode
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="QR Code Generator", 
    page_icon="📱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 2rem;
    }
    .input-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 2px solid #e9ecef;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .generate-button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📱 QR Code Generator</h1>', unsafe_allow_html=True)
# st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Create beautiful QR codes for URLs, text, or images with optional logo embedding</p>', unsafe_allow_html=True)

# Main input container
with st.container():
    # st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Content type selection
    col1, col2 = st.columns([1, 3])
    with col1:
        content_type = st.selectbox(
            "Content Type:",
            ["🔗 URL", "📝 Text", "🖼️ Image URL"],
            help="Select what type of content you want to encode"
        )
    
    with col2:
        # Dynamic placeholder based on content type
        if content_type == "🔗 URL":
            placeholder = "Enter website URL (e.g., https://www.example.com)"
            help_text = "Enter a valid website URL starting with http:// or https://"
        elif content_type == "📝 Text":
            placeholder = "Enter any text you want to encode"
            help_text = "Enter any text, message, or information you want to encode"
        else:  # Image URL
            placeholder = "Enter image URL (e.g., https://example.com/image.jpg)"
            help_text = "Enter a direct URL to an image file"
    
    # Main input field
    input_text = st.text_area(
        "Content to encode:",
        height=100,
        placeholder=placeholder,
        help=help_text
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced options in an expandable section
with st.expander("⚙️ Advanced Options", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        # Logo upload
        logo_file = st.file_uploader(
            "📷 Logo (Optional):",
            type=["png", "jpg", "jpeg"],
            help="Upload a logo to embed in the center of your QR code"
        )
        
        # QR code version
        qr_version = st.slider(
            'QR Code Complexity:',
            min_value=1, max_value=10, value=4,
            help="Higher values allow more data but create denser QR codes"
        )
    
    with col2:
        # Box size
        box_size = st.slider(
            'QR Code Size:',
            min_value=5, max_value=15, value=10,
            help="Larger values create bigger QR codes"
        )
        
        # Error correction level
        error_correction = st.selectbox(
            "Error Correction:",
            ["High (30%)", "Medium (15%)", "Low (7%)"],
            index=0,
            help="Higher correction allows for damaged QR codes to still work"
        )

# Generate button
st.markdown("<br>", unsafe_allow_html=True)
generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
with generate_col2:
    generate_button = st.button("🚀 Generate QR Code", use_container_width=True)

# Generation logic
if generate_button:
    if input_text.strip():
        # Validate input based on content type
        valid_input = True
        if content_type == "🔗 URL" and not (input_text.startswith("http://") or input_text.startswith("https://")):
            st.error("⚠️ Please enter a valid URL starting with http:// or https://")
            valid_input = False
        
        if valid_input:
            # Set error correction level
            error_levels = {
                "High (30%)": qrcode.constants.ERROR_CORRECT_H,
                "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
                "Low (7%)": qrcode.constants.ERROR_CORRECT_L
            }
            
            try:
                # Create QR code
                qr = qrcode.QRCode(
                    version=qr_version,
                    error_correction=error_levels[error_correction],
                    box_size=box_size,
                    border=4,
                )
                qr.add_data(input_text.strip())
                qr.make(fit=True)

                # Generate QR code image
                img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

                # Add logo if provided
                if logo_file:
                    try:
                        logo = Image.open(logo_file)
                        # Calculate logo size (1/5th of QR code for better proportion)
                        qr_size = img_qr.size[0]
                        logo_size = qr_size // 5
                        
                        # Resize logo maintaining aspect ratio
                        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
                        
                        # Create a white background for the logo area
                        logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
                        logo_bg_pos = ((logo_bg.size[0] - logo.size[0]) // 2, 
                                      (logo_bg.size[1] - logo.size[1]) // 2)
                        
                        if logo.mode == 'RGBA':
                            logo_bg.paste(logo, logo_bg_pos, logo)
                        else:
                            logo_bg.paste(logo, logo_bg_pos)
                        
                        # Calculate position to paste logo at center
                        pos = ((qr_size - logo_bg.size[0]) // 2, 
                              (qr_size - logo_bg.size[1]) // 2)
                        
                        img_qr.paste(logo_bg, pos)
                        st.success("✅ Logo successfully embedded!")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing logo: {e}")

                # Display results
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 🎉 Your QR Code is Ready!")
                
                # Show the QR code in a centered column
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(img_qr, caption="Generated QR Code", use_container_width=True)
                
                # Download section
                st.markdown("### 📥 Download")
                buf = io.BytesIO()
                img_qr.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
                with download_col2:
                    st.download_button(
                        label="⬇️ Download QR Code",
                        data=byte_im,
                        file_name=f"qr_code_{content_type.split()[1].lower()}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                # Show encoded content info
                with st.expander("ℹ️ QR Code Information"):
                    st.write(f"**Content Type:** {content_type}")
                    st.write(f"**Encoded Content:** {input_text[:50]}{'...' if len(input_text) > 50 else ''}")
                    st.write(f"**QR Version:** {qr_version}")
                    st.write(f"**Error Correction:** {error_correction}")
                    st.write(f"**Dimensions:** {img_qr.size[0]} x {img_qr.size[1]} pixels")
                
            except Exception as e:
                st.error(f"❌ Error generating QR code: {e}")
                st.info("💡 Try reducing the amount of text or selecting a higher QR code version.")
    else:
        st.warning("⚠️ Please enter some content to generate a QR code.")

# Footer with tips
st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("💡 Tips for Better QR Codes"):
    st.markdown("""
    **🎯 Best Practices:**
    - **URLs:** Always include http:// or https:// for web links
    - **Text:** Keep text concise for better scanning reliability
    - **Logos:** Use square images with transparent backgrounds for best results
    - **Size:** Larger QR codes are easier to scan from distance
    - **Testing:** Always test your QR code with a scanner before using
    
    **📱 Scanning Tips:**
    - Ensure good lighting when scanning
    - Hold device steady and at appropriate distance
    - Clean QR code surface if printed
    """)

# Quick actions sidebar
with st.sidebar:
    st.markdown("### 🔧 Quick Actions")
    if st.button("🔄 Clear All", use_container_width=True):
        st.rerun()
    
    st.markdown("### 📊 Usage Stats")
    st.info("QR codes can store:\n- URLs: ~2000 characters\n- Text: ~4000 characters\n- Numbers: ~7000 digits")
    
    st.markdown("### 🆘 Need Help?")
    st.markdown("""
    **Common Issues:**
    - QR too dense? Lower the version number
    - Can't scan? Increase error correction
    - Logo too big? It's auto-resized for optimal scanning
    """)