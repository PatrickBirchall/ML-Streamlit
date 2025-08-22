import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Music League Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess all CSV data"""
    try:
        # Load data
        competitors = pd.read_csv('data/competitors.csv')
        rounds = pd.read_csv('data/rounds.csv')
        submissions = pd.read_csv('data/submissions.csv')
        votes = pd.read_csv('data/votes.csv')

        # Convert dates
        rounds['Created'] = pd.to_datetime(rounds['Created'])
        submissions['Created'] = pd.to_datetime(submissions['Created'])
        votes['Created'] = pd.to_datetime(votes['Created'])

        # Merge data for analysis
        submissions_with_rounds = submissions.merge(
            rounds[['ID', 'Name']],
            left_on='Round ID',
            right_on='ID',
            suffixes=('', '_round')
        )

        votes_with_submissions = votes.merge(
            submissions_with_rounds[
                ['Spotify URI', 'Title', 'Artist(s)',
                 'Round ID', 'Name', 'Comment']
            ],
            on='Spotify URI',
            suffixes=('', '_submission')
        )

        votes_with_voters = votes_with_submissions.merge(
            competitors[['ID', 'Name']],
            left_on='Voter ID',
            right_on='ID',
            suffixes=('', '_voter')
        )

        return competitors, rounds, submissions, votes, votes_with_voters, submissions_with_rounds

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None

def main():
    # Header
    st.markdown(
        '<h1 class="main-header">🎵 Music League Analytics</h1>',
        unsafe_allow_html=True
    )

    # Load data
    competitors, rounds, submissions, votes, votes_with_voters, submissions_with_rounds = load_data()

    if competitors is None:
        st.error("Failed to load data. Please check your CSV files.")
        return

    # Debug: Print column names to help identify issues
    if st.checkbox("Debug: Show column names"):
        st.write("**votes_with_voters columns:**", list(votes_with_voters.columns))
        st.write("**submissions_with_rounds columns:**", list(submissions_with_rounds.columns))
        st.write("**filtered_votes columns:**", list(votes_with_voters.columns))
        st.write("**filtered_submissions columns:**", list(submissions_with_rounds.columns))

    # Sidebar filters
    st.sidebar.header("📊 Filters")

    # Round filter
    round_names = ['All Rounds'] + rounds['Name'].tolist()
    selected_round = st.sidebar.selectbox("Select Round", round_names)

    # Competitor filter
    competitor_names = ['All Competitors'] + competitors['Name'].tolist()
    selected_competitor = st.sidebar.selectbox("Select Competitor", competitor_names)

    # Apply filters
    if selected_round != 'All Rounds':
        round_id = rounds[rounds['Name'] == selected_round]['ID'].iloc[0]
        filtered_votes = votes_with_voters[votes_with_voters['Round ID'] == round_id]
        filtered_submissions = submissions_with_rounds[submissions_with_rounds['Round ID'] == round_id]
    else:
        filtered_votes = votes_with_voters
        filtered_submissions = submissions_with_rounds

    if selected_competitor != 'All Competitors':
        competitor_id = competitors[competitors['Name'] == selected_competitor]['ID'].iloc[0]
        filtered_votes = filtered_votes[filtered_votes['Voter ID'] == competitor_id]
        filtered_submissions = filtered_submissions[filtered_submissions['Submitter ID'] == competitor_id]

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview",
        "🗳️ Voting Patterns",
        "💬 Comments Analysis",
        "🎯 Round Insights",
        "👥 Competitor Stats"
    ])

    with tab1:
        st.header("📊 League Overview")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(rounds)}</div>
                <div class="metric-label">Total Rounds</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(competitors)}</div>
                <div class="metric-label">Active Competitors</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(submissions)}</div>
                <div class="metric-label">Total Submissions</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(votes)}</div>
                <div class="metric-label">Total Votes Cast</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts row 1
        col1, col2 = st.columns(2)

        with col1:
            # Submissions per round
            submissions_per_round = submissions_with_rounds.groupby('Name').size().reset_index(name='Count')
            fig = px.bar(
                submissions_per_round,
                x='Name',
                y='Count',
                title="Submissions per Round",
                color='Count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Voting activity over time
            votes_over_time = votes.groupby(votes['Created'].dt.date).size().reset_index(name='Votes')
            votes_over_time['Date'] = pd.to_datetime(votes_over_time['Created'])
            fig = px.line(
                votes_over_time,
                x='Date',
                y='Votes',
                title="Voting Activity Over Time",
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Charts row 2
        col1, col2 = st.columns(2)

        with col1:
            # Points distribution
            fig = px.histogram(
                votes,
                x='Points Assigned',
                title="Distribution of Points Assigned",
                nbins=10,
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Top artists
            top_artists = submissions['Artist(s)'].value_counts().head(10)
            # Convert to dataframe for Plotly
            top_artists_df = pd.DataFrame({
                'Artist': top_artists.index,
                'Count': top_artists.values
            })
            fig = px.bar(
                top_artists_df,
                x='Count',
                y='Artist',
                orientation='h',
                title="Top 10 Artists by Submissions",
                color='Count',
                color_continuous_scale='plasma'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("🗳️ Voting Patterns Analysis")

        # Voting behavior insights
        col1, col2 = st.columns(2)

        with col1:
            # Average points per voter
            avg_points_per_voter = filtered_votes.groupby('Name_voter')['Points Assigned'].mean().sort_values(ascending=False)
            # Convert to dataframe for Plotly
            avg_points_df = pd.DataFrame({
                'Voter': avg_points_per_voter.index,
                'Avg_Points': avg_points_per_voter.values
            })
            fig = px.bar(
                avg_points_df,
                x='Avg_Points',
                y='Voter',
                orientation='h',
                title="Average Points per Voter",
                color='Avg_Points',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Voting consistency (standard deviation)
            voting_consistency = filtered_votes.groupby('Name_voter')['Points Assigned'].agg(['mean', 'std']).reset_index()
            voting_consistency['std'] = voting_consistency['std'].fillna(0)
            fig = px.scatter(
                voting_consistency,
                x='mean',
                y='std',
                title="Voting Consistency (Mean vs Standard Deviation)",
                hover_data=['Name_voter'],
                labels={'mean': 'Average Points', 'std': 'Standard Deviation'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap of voting patterns
        st.subheader("🔥 Voting Pattern Heatmap")

        # Create voting matrix
        voting_matrix = filtered_votes.pivot_table(
            index='Name_voter',
            columns='Name',
            values='Points Assigned',
            aggfunc='mean',
            fill_value=0
        )

        fig = px.imshow(
            voting_matrix,
            title="Voting Pattern Heatmap (Average Points)",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Points distribution by round
        if selected_round == 'All Rounds':
            st.subheader("📊 Points Distribution by Round")
            points_by_round = votes_with_voters.groupby('Name')['Points Assigned'].agg(['mean', 'count']).reset_index()
            points_by_round.columns = ['Round', 'Average Points', 'Total Votes']

            fig = px.scatter(
                points_by_round,
                x='Total Votes',
                y='Average Points',
                title="Round Performance: Total Votes vs Average Points",
                hover_data=['Round'],
                size='Total Votes',
                color='Average Points',
                color_continuous_scale='plasma'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("💬 Comments Analysis")

        # Comment statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            total_comments = len(filtered_submissions[filtered_submissions['Comment'].notna() & (filtered_submissions['Comment'] != '')])
            st.metric("Total Comments", total_comments)

        with col2:
            comment_rate = (total_comments / len(filtered_submissions)) * 100
            st.metric("Comment Rate", f"{comment_rate:.1f}%")

        with col3:
            avg_comment_length = filtered_submissions[filtered_submissions['Comment'].notna() & (filtered_submissions['Comment'] != '')]['Comment'].str.len().mean()
            st.metric("Avg Comment Length", f"{avg_comment_length:.0f} chars")

        # Comment patterns
        col1, col2 = st.columns(2)

        with col1:
            # Comments per round
            comments_per_round = filtered_submissions.groupby('Name').agg(
                Comment_Count=('Comment', lambda x: (x.notna() & (x != '')).sum())
            ).reset_index()

            fig = px.bar(
                comments_per_round,
                x='Name',
                y='Comment_Count',
                title="Comments per Round",
                color='Comment_Count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Comment length distribution
            comment_lengths = filtered_submissions[filtered_submissions['Comment'].notna() & (filtered_submissions['Comment'] != '')]['Comment'].str.len()
            fig = px.histogram(
                x=comment_lengths,
                title="Comment Length Distribution",
                nbins=20,
                color_discrete_sequence=['#ff7f0e']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Most active commenters
        st.subheader("💭 Most Active Commenters")

        # Simple approach: get competitor names by looking up each Submitter ID
        submissions_with_comments = filtered_submissions[filtered_submissions['Comment'].notna() & (filtered_submissions['Comment'] != '')]

        commenter_names = []
        for _, submission in submissions_with_comments.iterrows():
            submitter_id = submission['Submitter ID']
            # Find the competitor with this ID
            competitor = competitors[competitors['ID'] == submitter_id]
            if len(competitor) > 0:
                commenter_names.append(competitor.iloc[0]['Name'])
            else:
                commenter_names.append(f"Unknown ({submitter_id})")

        # Create a simple series for top commenters
        if commenter_names:
            top_commenters = pd.Series(commenter_names).value_counts().head(10)
            st.success("Successfully retrieved competitor names")
        else:
            st.warning("No comments found")
            top_commenters = pd.Series()

        # Remove old code that references undefined 'commenters' variable
        # Convert to dataframe for Plotly
        top_commenters_df = pd.DataFrame({
            'Name': top_commenters.index,
            'Count': top_commenters.values
        })
        fig = px.bar(
            top_commenters_df,
            x='Count',
            y='Name',
            orientation='h',
            title="Top 10 Commenters",
            color='Count',
            color_continuous_scale='plasma'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Sample comments
        st.subheader("📝 Sample Comments")
        # Get comments first, then sample
        comments_only = filtered_submissions[filtered_submissions['Comment'].notna() & (filtered_submissions['Comment'] != '')]
        if len(comments_only) > 0:
            sample_size = min(5, len(comments_only))
            sample_comments = comments_only.sample(sample_size)
            
            for _, row in sample_comments.iterrows():
                with st.expander(f"🎵 {row['Title']} - {row['Artist(s)']}"):
                    st.write(f"**Comment:** {row['Comment']}")
                    # Get round name from the submissions_with_rounds data
                    round_name = submissions_with_rounds[submissions_with_rounds['Spotify URI'] == row['Spotify URI']]['Name'].iloc[0] if len(submissions_with_rounds[submissions_with_rounds['Spotify URI'] == row['Spotify URI']]) > 0 else "Unknown Round"
                    st.write(f"**Round:** {round_name}")
        else:
            st.info("No comments found for the selected filters.")

    with tab4:
        st.header("🎯 Round-Specific Insights")

        if selected_round == 'All Rounds':
            st.info("Select a specific round from the sidebar to see detailed insights.")

            # Show round comparison
            round_stats = []
            for _, round_data in rounds.iterrows():
                round_submissions = submissions[submissions['Round ID'] == round_data['ID']]
                round_votes = votes[votes['Round ID'] == round_data['ID']]

                stats = {
                    'Round': round_data['Name'],
                    'Submissions': len(round_submissions),
                    'Total Votes': len(round_votes),
                    'Avg Points': round_votes['Points Assigned'].mean(),
                    'Comments': len(round_submissions[round_submissions['Comment'].notna() & (round_submissions['Comment'] != '')])
                }
                round_stats.append(stats)

            round_df = pd.DataFrame(round_stats)

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    round_df,
                    x='Round',
                    y='Submissions',
                    title="Submissions per Round",
                    color='Submissions',
                    color_continuous_scale='viridis'
                )
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(
                    round_df,
                    x='Round',
                    y='Total Votes',
                    title="Total Votes per Round",
                    color='Total Votes',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)

        else:
            # Round-specific analysis
            st.subheader(f"📊 Analysis for: {selected_round}")

            round_id = rounds[rounds['Name'] == selected_round]['ID'].iloc[0]
            round_submissions = submissions[submissions['Round ID'] == round_id]
            round_votes = votes[votes['Round ID'] == round_id]

            # Round metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Submissions", len(round_submissions))

            with col2:
                st.metric("Total Votes", len(round_votes))

            with col3:
                st.metric("Avg Points", f"{round_votes['Points Assigned'].mean():.2f}")

            with col4:
                comment_count = len(round_submissions[round_submissions['Comment'].notna() & (round_submissions['Comment'] != '')])
                st.metric("Comments", comment_count)

            # Top submissions by points
            st.subheader("🏆 Top Submissions by Points")
            submission_points = round_votes.groupby('Spotify URI')['Points Assigned'].sum().reset_index()
            submission_points = submission_points.merge(
                round_submissions[['Spotify URI', 'Title', 'Artist(s)', 'Comment']],
                on='Spotify URI'
            ).sort_values('Points Assigned', ascending=False)

            fig = px.bar(
                submission_points.head(10),
                x='Points Assigned',
                y='Title',
                orientation='h',
                title="Top 10 Submissions by Total Points",
                color='Points Assigned',
                color_continuous_scale='viridis',
                hover_data=['Artist(s)', 'Comment']
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Voting distribution
            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(
                    round_votes,
                    x='Points Assigned',
                    title="Points Distribution",
                    nbins=10,
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Voter participation
                voter_participation = round_votes.groupby('Voter ID').size().reset_index(name='Votes_Cast')
                
                # Debug: Check voter participation columns
                if st.checkbox("Debug: Show voter participation columns"):
                    st.write("**voter_participation before merge:**", list(voter_participation.columns))
                    st.write("**competitors columns:**", list(competitors.columns))
                
                voter_participation = voter_participation.merge(
                    competitors[['ID', 'Name']],
                    left_on='Voter ID',
                    right_on='ID',
                    how='left'
                )
                
                # Debug: Check after merge
                if st.checkbox("Debug: Show merged voter participation"):
                    st.write("**voter_participation after merge:**", list(voter_participation.columns))
                    st.write("**voter_participation head:**", voter_participation.head())

                fig = px.bar(
                    voter_participation,
                    x='Name',
                    y='Votes_Cast',
                    title="Voter Participation",
                    color='Votes_Cast',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("👥 Competitor Statistics")

        if selected_competitor == 'All Competitors':
            st.info("Select a specific competitor from the sidebar to see detailed stats.")

            # Overall competitor rankings
            competitor_stats = []

            for _, competitor in competitors.iterrows():
                # Submissions
                comp_submissions = submissions[submissions['Submitter ID'] == competitor['ID']]
                submission_count = len(comp_submissions)

                # Votes received
                comp_votes = votes.merge(
                    submissions[['Spotify URI', 'Submitter ID']],
                    on='Spotify URI'
                )
                comp_votes = comp_votes[comp_votes['Submitter ID'] == competitor['ID']]
                total_points_received = comp_votes['Points Assigned'].sum()
                avg_points_received = comp_votes['Points Assigned'].mean() if len(comp_votes) > 0 else 0

                # Voting activity
                comp_voting = votes[votes['Voter ID'] == competitor['ID']]
                voting_count = len(comp_voting)
                avg_points_given = comp_voting['Points Assigned'].mean() if voting_count > 0 else 0

                # Comments
                comment_count = len(comp_submissions[comp_submissions['Comment'].notna() & (comp_submissions['Comment'] != '')])

                stats = {
                    'Name': competitor['Name'],
                    'Submissions': submission_count,
                    'Points Received': total_points_received,
                    'Avg Points Received': avg_points_received,
                    'Votes Cast': voting_count,
                    'Avg Points Given': avg_points_given,
                    'Comments': comment_count
                }
                competitor_stats.append(stats)

            comp_df = pd.DataFrame(competitor_stats)

            # Top competitors by different metrics
            col1, col2 = st.columns(2)

            with col1:
                top_submitters = comp_df.nlargest(10, 'Submissions')
                fig = px.bar(
                    top_submitters,
                    x='Submissions',
                    y='Name',
                    orientation='h',
                    title="Top 10 Submitters",
                    color='Submissions',
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                top_point_receivers = comp_df.nlargest(10, 'Points Received')
                fig = px.bar(
                    top_point_receivers,
                    x='Points Received',
                    y='Name',
                    orientation='h',
                    title="Top 10 Point Receivers",
                    color='Points Received',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            # Scatter plot: Submissions vs Points Received
            fig = px.scatter(
                comp_df,
                x='Submissions',
                y='Points Received',
                title="Submissions vs Points Received",
                hover_data=['Name', 'Avg Points Received'],
                size='Comments',
                color='Votes Cast',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        else:
            # Individual competitor analysis
            st.subheader(f"👤 Analysis for: {selected_competitor}")

            competitor_id = competitors[competitors['Name'] == selected_competitor]['ID'].iloc[0]

            # Competitor metrics
            comp_submissions = submissions[submissions['Submitter ID'] == competitor_id]
            comp_votes_received = votes.merge(
                submissions[['Spotify URI', 'Submitter ID']],
                on='Spotify URI'
            )
            comp_votes_received = comp_votes_received[comp_votes_received['Submitter ID'] == competitor_id]
            comp_votes_cast = votes[votes['Voter ID'] == competitor_id]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Submissions", len(comp_submissions))

            with col2:
                st.metric("Points Received", comp_votes_received['Points Assigned'].sum())

            with col3:
                st.metric("Votes Cast", len(comp_votes_cast))

            with col4:
                comment_count = len(comp_submissions[comp_submissions['Comment'].notna() & (comp_submissions['Comment'] != '')])
                st.metric("Comments", comment_count)

            # Submission performance
            st.subheader("📊 Submission Performance")
            submission_performance = comp_submissions.merge(
                comp_votes_received.groupby('Spotify URI')['Points Assigned'].sum().reset_index(name='Total_Points'),
                on='Spotify URI',
                how='left'
            ).fillna(0)

            fig = px.bar(
                submission_performance,
                x='Title',
                y='Total_Points',
                title="Points Received per Submission",
                color='Total_Points',
                color_continuous_scale='viridis',
                hover_data=['Artist(s)', 'Comment']
            )
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Voting behavior
            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(
                    comp_votes_cast,
                    x='Points Assigned',
                    title="Voting Distribution",
                    nbins=10,
                    color_discrete_sequence=['#ff7f0e']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Voting by round
                # Get votes with round information by merging with the full votes_with_voters data
                comp_votes_with_rounds = votes_with_voters[votes_with_voters['Voter ID'] == competitor_id]
                voting_by_round = comp_votes_with_rounds.groupby('Name')['Points Assigned'].agg(['mean', 'count']).reset_index()
                voting_by_round.columns = ['Round', 'Avg Points', 'Votes Cast']

                fig = px.bar(
                    voting_by_round,
                    x='Round',
                    y='Avg Points',
                    title="Average Points Given by Round",
                    color='Votes Cast',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>🎵 Music League Analytics Dashboard | Built with Streamlit & Plotly</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
