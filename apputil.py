import plotly.express as px
import pandas as pd

def survival_demographics():
    """Creates a Dataframe with survival statistics by passenger class, sex, and age group ordered for easy interpretation."""

    # Read in titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Use pd.cut to create age groups based on the Age column
    df['Age_Group'] = pd.cut(df["Age"], bins = [0, 12, 19, 59, float("inf")], labels = ["child", "teen", "adult", "senior"])

    # Group the passangers by class, sex, and group
    df_grouped = df.groupby(['Pclass', 'Sex', 'Age_Group']).agg(
        Survived_Count=('Survived','sum'),
        Passenger_Count=('PassengerId', 'count')
    ).reset_index()

    # Calculate survival percentage
    df_grouped['Survival_Percentage'] = ((df_grouped['Survived_Count'] / df_grouped['Passenger_Count']) * 100).round(2)
    
    df_grouped = df_grouped.sort_values(by='Survival_Percentage', ascending=False)

    return df_grouped

def visualize_demographic():
    """Creates a Plotly figure comparing survival rates of 1st class men, 3rd class children, and 3rd class men."""

    # Get the Dataframe
    df_viz = survival_demographics()

    # Create the two categories for visualization analysis.
    df_viz['Category'] = "Other"
    df_viz.loc[(df_viz['Pclass'] == 1) & (df_viz['Sex'] == 'male') & (df_viz['Age_Group'] != 'child'), 'Category'] = '1st Class Male'
    df_viz.loc[(df_viz['Pclass'] == 3) & (df_viz['Age_Group'] == 'child'), 'Category'] = '3rd Class Child'
    df_viz.loc[(df_viz['Pclass'] == 3) & (df_viz['Sex'] == 'male') & (df_viz['Age_Group'] != 'child'), 'Category'] = '3rd Class Male'

    # Filter the Dataframe for the visualization
    df_viz = df_viz[df_viz['Category'] != "Other"]

    # Group by Category and Get Summative Numbers
    df_viz = df_viz.groupby('Category', as_index = False).agg({
        'Survived_Count' : "sum",
        'Passenger_Count' : "sum"
    })

    # Calculate Survival Rate
    df_viz["Survival Percentage"] = round((df_viz["Survived_Count"]/df_viz["Passenger_Count"] * 100), 2)

    # Create the figure
    fig = px.bar(
        df_viz,  
        title='Was surviving the Titanic Fair?',
        subtitle='Comparing survival rates for 1st class men, 3rd class children, and 3rd class men.',
            x='Category',
            y='Survival Percentage',
            text='Survival Percentage',
            hover_data={
            'Category': True,
            'Survived_Count': True,
            'Passenger_Count': True,
            'Survival Percentage': ":.1f"
        },
            template='simple_white',
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
    """Returns a pandas series with the count of passangers that have the same last name."""

    # Read in titanic datasets
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Create a last name column
    df['last_name'] = df['Name'].apply(lambda x: x.split(',')[0].strip())

    # Group passengers by last name and compute total count
    last_names = df["last_name"].value_counts()

    return last_names

def family_size():
    """Creates the basic dataframe with family size information."""

    # Read in titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Add a family size column and a count column
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    df['Count'] = 1

    return df
    
def visualize_family_size_comparison():
    """Creates a Plotly figure visualizing family size distribution by passenger class."""

    # Get the Dataframe(s)
    df_viz_last_names = last_names()
    df_viz_family_size = family_size()

    # Adjust last name data frame
    df_viz_last_names = df_viz_last_names.reset_index()
    df_viz_last_names.columns = ["last_name", "family_size"]
    df_viz_last_names['group'] = 'Last_Names'
    df_viz_last_names = df_viz_last_names.groupby(["group", "family_size"], as_index=False).size().rename(columns={"size": "count"})

    # Adjust family size data frame
    df_viz_family_size['group'] = 'family_calc'
    df_viz_family_size = df_viz_family_size[['group', 'family_size']]
    df_viz_family_size = df_viz_family_size.groupby(["group", "family_size"], as_index=False).size().rename(columns={"size": "count"})

    df_all = pd.concat([df_viz_last_names, df_viz_family_size], ignore_index=True)

    # Create the figure
    fig = px.bar(
        df_all,
        x='family_size',
        y = 'count',
        color='group',
        barmode='group',
        template='simple_white',
        title='Family Size Distribution by Method',
        subtitle='Discrepancies likely caused by repeated counts present within the family size computation method that would not be present in the last name method.',
        color_discrete_sequence=px.colors.qualitative.D3
    )
    
    return fig

def visualize_families():
    """Creates a Plotly figure visualizing family size and the probability of survival."""

    df = family_size()
    df = df[['family_size','Survived']].groupby(['family_size', 'Survived']).value_counts().reset_index()
    df['percentage'] = round(df['count'] / df.groupby('family_size')['count'].transform('sum') * 100,2)
    df['Survived'] = df['Survived'].map({
        0: 'dead',
        1: 'alive'
    })

    fig = px.bar(
        df,
        x = 'family_size',
        y = 'percentage',
        color = 'Survived',
        barmode = 'stack',
        text='percentage',
        template='simple_white',
        title='Percentage of Titanic Passengers that survived by Family Size',
        color_discrete_map={
            'dead': 'gray',
            'alive': 'blue'
        },
        category_orders={
            'Survived':['alive','dead']
        },
        hover_data = {
            'family_size': True,
            'count': True,
            'percentage': True,
            'Survived': True
        },
        labels={
            'family_size' : 'Family Size',
            'percentage' : 'Percent of Passengers'
        }
    )

    return fig
    
def determin_age_division():
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    df['older_passenger'] = df['Age'] > df.groupby('Pclass')['Age'].transform('median')

    return df

def visualize_age_division():
    df = determin_age_division()

    df = df[['older_passenger', 'Survived']]

    prob_matrix = pd.crosstab(
        index=df['older_passenger'],
        columns=df['Survived'],
        normalize='index'
    ) * 100

    prob_matrix = prob_matrix.round(1)

    prob_matrix = prob_matrix.rename(
        index={False: 'Younger', True: 'Older'},
        columns={0: 'Died', 1: 'Survived'}
    )

    fig = px.imshow(
        prob_matrix,
        text_auto='.1f',
        color_continuous_scale='Blues',
        aspect='auto',
        labels={
            'x': 'Outcome',
            'y': 'Passenger Group',
            'color': 'Percent'
        },
        title='Survival Rate by Passenger Age Group'
    )

    fig.update_traces(
        texttemplate='%{z:.1f}%',
        hovertemplate='Passenger Group: %{y}<br>Outcome: %{x}<br>Percent: %{z:.1f}%<extra></extra>'
    )

    fig.update_layout(
        xaxis_title='Outcome',
        yaxis_title='Passenger Group',
        coloraxis_colorbar_title='Percent',
        title_x=0.5
    )

    return fig