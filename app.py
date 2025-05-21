import streamlit as st
import sys
import os
import time

# Add the blogger directory to Python path so we can import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'TTS', 'blogger'))

from workingtest01 import generate_blogger_content
from blogy import authenticate, post_to_blogger

st.set_page_config(page_title="Blog Generator", layout="wide")

st.title("✍️ AI Blog Generator")

# Initialize session state for tracking
if 'blog_content' not in st.session_state:
    st.session_state.blog_content = None
if 'seo_content' not in st.session_state:
    st.session_state.seo_content = None
if 'title' not in st.session_state:
    st.session_state.title = None
if 'category' not in st.session_state:
    st.session_state.category = None
if 'post_url' not in st.session_state:
    st.session_state.post_url = None

# Input section
st.subheader("Blog Details")
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("Enter Blog Topic:", placeholder="e.g., Artificial Intelligence in Healthcare")

with col2:
    image_count = st.slider("Number of Images:", min_value=1, max_value=5, value=3)

# Status display section
status_container = st.empty()
progress_bar = st.empty()

# Generation section
if st.button("Generate Blog 🎨", type="primary"):
    if not topic:
        st.warning("Please enter a blog topic!")
    else:
        progress = 0
        progress_bar_value = progress_bar.progress(progress, "Starting blog generation...")
        
        try:
            # Step 1: Generate content
            status_container.info("🤖 Generating blog content and images...")
            generate_blogger_content(topic, image_count)
            progress += 50
            progress_bar_value.progress(progress, "Content generated...")
            
            # Read the generated files
            with open("blogger_final.html", "r", encoding="utf-8") as f:
                blog_content = f.read()
                st.session_state.blog_content = blog_content
                
            with open("blogger_seo.txt", "r", encoding="utf-8") as f:
                seo_content = f.read()
                st.session_state.seo_content = seo_content
                # Parse SEO content
                title = ""
                category = "Technology"
                for line in seo_content.split("\n"):
                    if line.startswith("Title:"):
                        title = line.replace("Title:", "").strip()
                    elif line.startswith("Category:"):
                        category = line.replace("Category:", "").strip()
                st.session_state.title = title
                st.session_state.category = category
            
            progress = 100
            progress_bar_value.progress(progress, "Ready for preview!")
            status_container.success("✅ Blog content generated successfully!")
            
        except Exception as e:
            status_container.error(f"❌ Error: {str(e)}")
            progress_bar_value.empty()

# Show preview and edit section if content is generated
if st.session_state.blog_content:
    st.markdown("---")
    
    # SEO Information in expander
    with st.expander("SEO Information"):
        st.text(st.session_state.seo_content)
    
    # Preview section
    st.subheader("Preview & Edit")
    
    # Edit area
    edited_content = st.text_area(
        "Edit your blog content here:",
        value=st.session_state.blog_content,
        height=400
    )
    
    # Update session state with edited content
    st.session_state.blog_content = edited_content
    
    # Preview button and area
    if st.button("Preview Blog 👀"):
        st.subheader("Live Preview")
        st.components.v1.html(edited_content, height=600, scrolling=True)
    
    # Publish section
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("Publish Blog 🚀", type="primary"):
            status_container.info("🌐 Connecting to Blogger...")
            try:
                # Authenticate
                service = authenticate()
                
                # Publish post
                status_container.info("📤 Publishing your blog post...")
                post = post_to_blogger(
                    service=service,
                    title=st.session_state.title,
                    content=edited_content,
                    labels=[st.session_state.category, "AI Generated", topic]
                )
                
                # Store post URL and show success
                st.session_state.post_url = post['url']
                status_container.success(f"""
                ✨ Blog Published Successfully!
                
                Title: {st.session_state.title}
                Category: {st.session_state.category}
                Status: Live
                
                🔗 [Click here to view your blog post]({post['url']})
                """)
                
            except Exception as e:
                status_container.error(f"❌ Publishing Error: {str(e)}")
    
    with col2:
        # Download option
        st.download_button(
            label="Download Blog HTML",
            data=edited_content,
            file_name="blog.html",
            mime="text/html"
        )

# Show last published post if available
if st.session_state.post_url:
    st.markdown("---")
    st.markdown("### 📝 Last Published Post")
    st.markdown(f"🔗 [View your last published post]({st.session_state.post_url})")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Google Gemini")
