import plotly.express as px
import pandas as pd

def survival_demographics():
    """Creates a Dataframe with survival statistics by passenger class, sex, and age group."""

    # Read in titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Use pd.cut to create age groups based on the Age column and a count column
    df['Age_Group'] = pd.cut(df["Age"], bins = [0, 12, 20, 60, 120], labels = ["child", "teen", "adult", "senior"])
    df['Count'] = 1

    # Group the passangers by class, sex, and group
    df_grouped = df.groupby(['Pclass', 'Sex', 'Age_Group'], observed=False).agg({
        'Survived': 'sum',
        'Count': 'sum'
    }).reset_index()

    # Calculate survival percentage
    df_grouped['Survival_Percentage'] = ((df_grouped['Survived'] / df_grouped['Count']) * 100).round(2)

    # Rename becuase of capital letter issues
    df_grouped = df_grouped.rename(columns={
        'Pclass': 'pclass',
        'Sex': 'sex',
        'Age_Group': 'age_group',
        'Survived': 'survived',
        'Count': 'n_survivors',
        'Survival_Percentage': 'survival_percentage'
    })

    return df_grouped

def visualize_demographic():
    """Creates a Plotly figure comparing survival rates of 1st class men with 3rd class children."""

    # Get the Dataframe
    df_viz = survival_demographics()

    # Create the two categories for visualization analysis.
    df_viz['category'] = "Other"
    df_viz.loc[(df_viz['pclass'] == 1) & (df_viz['sex'] == 'male'), 'category'] = '1st Class Male'
    df_viz.loc[(df_viz['pclass'] == 3) & (df_viz['age_group'] == 'child'), 'category'] = '3rd Class Child'

    # Filter the Dataframe for the visualization
    df_viz = df_viz[df_viz['category'] != "Other"]

    # Create the figure
    fig = px.histogram(
            df_viz,  
             y='survival_percentage',
             x='category',
             histfunc='avg',
             hover_data=['category'],
             template='plotly_white',
             color_discrete_sequence=px.colors.qualitative.D3
            )

    return fig

def family_groups():
    """"Creates a Dataframe with survival statistics by family size and passenger class."""

    # Read in titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Add a family size column and a count column
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    df['Count'] = 1

    # Group the passangers by family size and passenger class and compute basic statistics within each group
    df_grouped = df.groupby(['Pclass','family_size']).agg(
    n_passengers=('Count', 'sum'),
    avg_fare=('Fare', 'mean'),
    min_fare=('Fare', 'min'),
    max_fare=('Fare', 'max')
    ).reset_index()

    return df_grouped

def last_names():
    """Creates a Dataframe with survival statistics by last name"""

     # Read in titanic datasets
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Create a last name column
    df['last_name'] = df['Name'].apply(lambda x: x.split(',')[0].strip())
    df['Count'] = 1

    # Group passengers by last name and compute total count
    df_groupby = df.groupby('last_name')['Count'].sum()

    return df_groupby

def family_size():
    """Creates the basic dataframe with family size information."""

    # Read in titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Add a family size column and a count column
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    df['Count'] = 1

    return df
    
def visualize_families():
    """Creates a Plotly figure visualizing family size distribution by passenger class."""

    # Get the Dataframe(s)
    df_viz_last_names = last_names()
    df_viz_family_size = family_size()

    # Adjust the Dataframes for Combination and then combine
    df_viz_last_names['group'] = 'Last_Names'
    df_viz_family_size['group'] = 'Family_Size'

    df1 = df_viz_last_names.reset_index()        # converts Series to DataFrame
    df1 = df1.rename(columns={df1.columns[1]: 'family_size'})  # rename values column
    df1['group'] = 'Last_Names'
    df2 = df_viz_family_size[['group', 'family_size']]

    df_all = pd.concat([df1, df2], ignore_index=True)

    # Create the figure
    fig = px.histogram(df_all,
                       x='family_size',
                       color='group',
                       facet_row='group',
                       template='plotly_white',
                       )
    
    return fig

