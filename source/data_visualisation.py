import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.offsetbox as offsetbox
import os

class FootballVisualisation:
    def __init__(self, goals_df, folder_path):
        """
        Initialize the FootballVisualisation class with the goals DataFrame and folder path for player images.
        
        Parameters:
        goals_df (pd.DataFrame): DataFrame containing the goals data with players as rows and gameweeks as columns.
        folder_path (str): Path to the folder containing player images.
        """
        self.goals_df = goals_df
        self.folder_path = folder_path

    def plot_cumulative_goals_over_time(self):
        """
        Plot a line graph showing the cumulative goal count over time for each player and place player images
        at their final cumulative goal positions for the maximum gameweek.
        """
        # Set up the figure and axis with a white background color
        fig, ax = plt.subplots(figsize=(14, 8))  # Increased figure size
        ax.set_facecolor('white')  # White background color for a clean look

        # Plot each player's cumulative goals over time
        for player in self.goals_df['Player']:
            player_goals = self.goals_df[self.goals_df['Player'] == player].iloc[0, 1:]
            cumulative_goals = player_goals.cumsum()  # Calculate the cumulative sum of goals
            ax.plot(cumulative_goals.index, cumulative_goals.values, marker='o', linestyle='-', color='grey', alpha=0.5)

        # Determine the maximum gameweek and its index
        max_gameweek = self.goals_df.columns[-1]
        max_gameweek_index = self.goals_df.columns.get_loc(max_gameweek) + 1  # Index of the maximum gameweek

        # Adjust plot limits to add excess space on the right
        ax.set_xlim(self.goals_df.columns[1], self.goals_df.columns[-1])
        ax.set_ylim(0, self.goals_df.iloc[:, 1:].max().max() + 10)  # Extend y-axis to fit images

        # Place player images at their final cumulative goal positions for the maximum gameweek
        image_offsets = {}
        for player in self.goals_df['Player']:
            player_goals = self.goals_df[self.goals_df['Player'] == player].iloc[0, 1:]
            cumulative_goals = player_goals.cumsum()  # Calculate the cumulative sum of goals
            final_goals = cumulative_goals.iloc[-1]  # Final cumulative goals for the maximum gameweek

            # Load player image
            image_path = os.path.join(self.folder_path, f"{player.lower().replace(' ', '_')}.png")
            if os.path.isfile(image_path):
                img = mpimg.imread(image_path)
                
                # Create an OffsetImage object with increased size
                imagebox = offsetbox.OffsetImage(img, zoom=0.3)  # Increased zoom for larger images
                # Stack images if multiple players end up at the same cumulative goal count
                y_offset = image_offsets.get(final_goals, 0)
                image_offsets[final_goals] = y_offset + 0.3  # Update offset for stacking

                # Create AnnotationBbox to place the image on the plot
                ab = offsetbox.AnnotationBbox(imagebox, (max_gameweek_index - 1 + 0.5, final_goals - y_offset),
                                              frameon=False, pad=0.1, bboxprops=dict(facecolor='none'))
                ax.add_artist(ab)

        # Set graph title and labels
        ax.set_title('Cumulative Goals Scored Over Time by Player')
        ax.set_xlabel('Gameweek')
        ax.set_ylabel('Cumulative Goals Scored')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        im = plt.imread('player_images/player_5.png')
        implot = plt.imshow(im, origin='upper', aspect='auto', extent=[2.5,5,2.5,7.5], zorder=0)
        # Remove gridlines
        ax.grid(False)

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()
