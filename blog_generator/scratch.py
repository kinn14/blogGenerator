import streamlit as st
from app import BlogGeneratorGraph


st.title('Blog Generator')
st.write("Generates title and content for given topic")

# workflow = graph.invoke({"messages":topic})


# Initialize session state
if 'blog_state' not in st.session_state:
    st.session_state.blog_state = {
        "messages":[],
        "topic": None,
        "title": None,
        "u_feedback": None,
        "content": None
    }

topic = st.text_input("Enter a blog topic:", "")
graph = BlogGeneratorGraph().create_application_graph()



# def replace_text():
#     st.session_state["text"] = text1.replace(before, after)

if st.button("Generate Title"):
    if topic:
        st.subheader("Generated Title")
        new_state = graph.invoke({
            "messages":[topic],
            "topic": None,
            "title": None,
            "u_feedback": 'yes',
            "content": None
        })
        st.session_state.blog_state = new_state 
        st.text_area('Title : ', st.session_state.blog_state["title"])
        st.write(st.session_state.blog_state['title'])
    else:
        st.warning("Please enter a topic before generating a blog.")

if st.session_state.blog_state['title']:
    st.subheader("Suggested Title")
    st.write(f"💡 **{st.session_state.blog_state['title']}**")

    # user_fb = st.text_input(f"Are you happy with the title {st.session_state.blog_state['title']} (yes/no)", "")

    col1, col2 = st.columns(2)
    if col1.button("✅ Use this Title"):
        st.session_state.blog_state.u_feedback = 'yes'
        st.session_state.blog_state = graph.invoke(st.session_state.blog_state, start_at="feedback")
        st.subheader("Generated Content")
        st.write(st.session_state.blog_state['messages'][-1].content)

    if col2.button("🔁 Regenerate Title"):
        st.session_state.state.u_feedback = 'no'
        st.session_state.state = graph.invoke(st.session_state.state, start_at="feedback", end_at="feedback")

else:
    st.warning("Please enter if you  are happy or not with title, we can regenerate.")

    # if user_fb:
    #         st.session_state.blog_state['u_feedback'] = user_fb
    #         if user_fb == 'yes':
    # else:
