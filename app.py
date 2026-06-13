import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

##
## Question #1 
##

st.write(
'''
# Did men in the first class have a higher survival chance than children in the third class? How does this compare to third class men?

'''
)
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

##
## Question #2
##

st.write(
'''
# How do family sizes compare on the Titanic as reported by last names vs. calculated based on family size? Do they agree?
'''
)

# Generate and display the figure
fig2 = visualize_family_size_comparison()
st.plotly_chart(fig2, use_container_width=True)


##
## Question #3
##

st.write(
'''
# Is there any relationship between family size and survival?
'''
)

# Generate and display the figure
fig3 = visualize_families()
st.plotly_chart(fig3, use_container_width=True)

##
## Question #4
##
st.write(
'''
# How do older vs younger passengers fair in survival when accounting for passenger class?
'''
)
fig4 = visualize_age_division()
st.plotly_chart(fig4, use_container_width=True)