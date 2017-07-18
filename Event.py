from Constant import Constant
from Moment import Moment
from Team import Team
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np


class Event:
    """A class for handling and showing events"""

    def __init__(self, event):
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))

    def update_radius(self, i, player_circles, ball_circle,ax,annotations, clock_info):
        moment = self.moments[i]
        for j, circle in enumerate(player_circles):
            circle.center = moment.players[j].x, moment.players[j].y
            annotations[j].set_position(circle.center)
            # clock_test = 'Quarter {:d}\n {:02d}:{:02d}\n {:03.1f}'.format(
            #              moment.quarter,
            #              int(moment.game_clock) % 3600 // 60,
            #              int(moment.game_clock) % 60,
            #              moment.shot_clock)
            clock_test = ''
            clock_info.set_text(clock_test)
        ball_circle.center = moment.ball.x, moment.ball.y
        ball_circle.radius = 0.8 + moment.ball.radius / Constant.NORMALIZATION_COEF

        # clear previous frame lines
        for line in ax.lines:
            ax.lines.remove(line)

        # update guest team's  convex hull of full back play movements.
        vistor_player_id=[2682,2581,2664,2611]
        self.update_convexhull(ax, moment, vistor_player_id, False)

        #update home team's convex hull of full back play movements.
        home_player_id=[2677,2329,2629,2671]
        self.update_convexhull(ax, moment, home_player_id, True)

        return player_circles, ball_circle

    def update_convexhull(self, ax, moment, player_id, home):
        player_positions = []
        for player in moment.players:
            if player.id in player_id:
                player_positions.append([player.x, player.y])

        from scipy.spatial import ConvexHull
        player_positions = np.array(player_positions)
        hull = ConvexHull(player_positions)
        hull_lines = []
        import matplotlib.lines as mlines
        if home == True:
            for simplex in hull.simplices:
                hull_lines.append(
                    mlines.Line2D(player_positions[simplex, 0], player_positions[simplex, 1],color="#002082"))
        else:
            for simplex in hull.simplices:
                hull_lines.append(
                    mlines.Line2D(player_positions[simplex, 0], player_positions[simplex, 1], color="#E13A3E"))
        for line in hull_lines:
            ax.add_line(line)

    def show(self):
        # Leave some space for inbound passes
        ax = plt.axes(xlim=(Constant.X_MIN,
                            Constant.X_MAX),
                      ylim=(Constant.Y_MIN,
                            Constant.Y_MAX))
        ax.axis('off')
        fig = plt.gcf()
        ax.grid(False)  # Remove grid
        start_moment = self.moments[0]
        player_dict = self.player_ids_dict

        clock_info = ax.annotate('', xy=[Constant.X_CENTER, Constant.Y_CENTER],
                                 color='black', horizontalalignment='center',
                                   verticalalignment='center')

        annotations = [ax.annotate(self.player_ids_dict[player.id][1], xy=[0, 0], color='w',
                                   horizontalalignment='center',
                                   verticalalignment='center', fontweight='bold')
                       for player in start_moment.players]

        # Prepare table
        sorted_players = sorted(start_moment.players, key=lambda player: player.team.id)

        home_player = sorted_players[0]
        guest_player = sorted_players[5]
        column_labels = tuple([home_player.team.name, guest_player.team.name])
        column_colours = tuple([home_player.team.color, guest_player.team.color])
        cell_colours = [column_colours for _ in range(5)]

        home_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[:5]]
        guest_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[5:]]
        players_data = list(zip(home_players, guest_players))

        # table = plt.table(cellText=players_data,
        #                       colLabels=column_labels,
        #                       colColours=column_colours,
        #                       colWidths=[Constant.COL_WIDTH, Constant.COL_WIDTH],
        #                       loc='bottom',
        #                       cellColours=cell_colours,
        #                       fontsize=Constant.FONTSIZE,
        #                       cellLoc='center')
        # table.scale(1, Constant.SCALE)
        # table_cells = table.properties()['child_artists']
        # for cell in table_cells:
        #     cell._text.set_color('white')

        player_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color=player.color)
                          for player in start_moment.players]
        ball_circle = plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE,
                                 color=start_moment.ball.color)



        # player_postions = []
        # for player in start_moment.players:
        #     if player.team.id == 1:
        #         if player.id == 2682 or player.id == 2581 or player.id == 2664 or player.id == 2611:
        #             player_postions.append([player.x, player.y])
        # from scipy.spatial import ConvexHull
        # print(player_postions)
        # player_postions = np.array(player_postions)
        # hull = ConvexHull(player_postions)

        for circle in player_circles:
            ax.add_patch(circle)
        ax.add_patch(ball_circle)

        # hull_lines = []
        # import matplotlib.lines as mlines
        # for simplex in hull.simplices:
        #     hull_lines.append(mlines.Line2D(player_postions[simplex,0],player_postions[simplex,1]))
        #
        # for line in hull_lines:
        #     ax.add_line(line)

        # anim = animation.FuncAnimation(
        #                  fig, self.update_radius,
        #                  fargs=(player_circles, ball_circle, annotations, clock_info),
        #                  frames=len(self.moments), interval=Constant.INTERVAL)
        anim = animation.FuncAnimation(
                         fig, self.update_radius,
                         fargs=(player_circles, ball_circle ,ax, annotations, clock_info),
                         frames=len(self.moments), interval=40)
        court = plt.imread("football_court_small.png")
        plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
                                            Constant.Y_MAX, Constant.Y_MIN])
        anim.save('soccer-convexhull.gif', writer="imagemagick")
        plt.show()
