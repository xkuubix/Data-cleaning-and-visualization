# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


filename = r"gr lab 2.xlsx"
df = pd.read_excel(filename)


# %%
def plot_data(data: pd.DataFrame):
    data.fillna("missing", inplace=True)
    col_names = data.columns.to_list()
    map = data.applymap(lambda x: isinstance(x, (int, float)))
    fig, ax = plt.subplots(len(col_names)//2, 2)
    fig.set_figheight(15)
    fig.set_figwidth(20)
    for col in range(len(col_names)):
        ax[col // 2, col % 2].plot(data[map][col_names[col]], '.')
        ax[col // 2, col % 2].set_title(col_names[col])
        ax[col // 2, col % 2].set_ylabel(r'T [$^\circ$C]')
        ax[col // 2, col % 2].set_xlabel('sample')
        # good_values_count = map.sum()[col_names[col]]
        # good_values_sum = data[map][col_names[col]].sum()


def clear_data(data: pd.DataFrame):
    pd.options.mode.chained_assignment = None
    data.fillna("missing", inplace=True)
    col_names = data.columns.to_list()
    map = data.applymap(lambda x: isinstance(x, (int, float)))
    for col in range(len(col_names)):
        median_value = data[col_names[col]][map[col_names[col]]].median()
        data[col_names[col]][~ map[col_names[col]]] = median_value
        data[col_names[col]][data[col_names[col]] < 36] = median_value
        data[col_names[col]][data[col_names[col]] > 40] = median_value
        # print(data[col_names[col]][~ map[col_names[col]]])
    data = data.astype('float64')
    return data


def print_data_stats(data: pd.DataFrame):
    columns_titles = ['S1_TC1', 'S2_TC1', 'S3_TC1',
                      'S1_TC2', 'S2_TC2', 'S3_TC2']
    data = data.reindex(columns=columns_titles)
    col_names = data.columns.to_list()
    print('\nName	mean	   std	      range	     median', end='')
    print('	    skewness   curtosis   mode[s]')
    for col in range(len(col_names)):
        data_mean = data[col_names[col]].mean()
        data_std = data[col_names[col]].std()
        data_max = data[col_names[col]].max()
        data_min = data[col_names[col]].min()
        data_range = data_max - data_min
        data_mode = data[col_names[col]].mode()
        data_median = data[col_names[col]].median()
        data_skewness = data[col_names[col]].skew()
        data_curtosis = data[col_names[col]].kurtosis()
        print(f'{col_names[col]:7} {data_mean:5.6f}  ' +
              f'{data_std:5.6f}   {data_range:5.6f}   {data_median:5.6f} ' +
              f'{data_skewness: 5.6f}  {data_curtosis: 5.6f}', end='')
        for item in data_mode:
            print(f'  {item: 2.6f}', end=' ')
        print()


def plot_hist(data: pd.DataFrame):
    data.fillna("missing", inplace=True)
    col_names = data.columns.to_list()
    map = data.applymap(lambda x: isinstance(x, (int, float)))
    fig, ax = plt.subplots(len(col_names)//2, 2)
    fig.set_figheight(15)
    fig.set_figwidth(20)
    for col in range(len(col_names)):
        ax[col // 2, col % 2].hist(data[map][col_names[col]], bins=20)
        ax[col // 2, col % 2].set_title(col_names[col])
        ax[col // 2, col % 2].set_ylabel('n_samples')
        ax[col // 2, col % 2].set_xlabel(r'T [$^\circ$C]')

    columns_titles = ['S1_TC1', 'S2_TC1', 'S3_TC1',
                      'S1_TC2', 'S2_TC2', 'S3_TC2']
    d1 = data.reindex(columns=columns_titles[0:3])
    one_sensor_plot(d1, columns_titles[0:3])
    d2 = data.reindex(columns=columns_titles[3:])
    one_sensor_plot(d2, columns_titles[3:])


def one_sensor_plot(d: pd.DataFrame, columns_titles):
    d = d.reindex(columns=columns_titles)
    sns.set_theme(style="ticks")
    colors = ['#0000FF', '#00FF00', '#FF0000']
    f, ax = plt.subplots()
    sns.despine(f)
    sns.histplot(
        d,
        multiple='layer',
        edgecolor=".3",
        linewidth=.5,
        color=colors,
        bins=20
        )
    # ax.set_xticks([36.5, 37, 37.5, 38])
    ax.set_xlabel(r'T [$^\circ$C]')
    ax.set_yscale('log')
    ax.grid(visible=True, which='both')
    # ylim = ax.get_ylim()
    # i = 0
    # for d_mean, d_std in zip(d.mean(), d.std()):
    #     ax.vlines(d_mean, ymin=10, ymax=9990,
    #               linestyles='dashed',
    #               color=colors[i])
    #     ax.vlines(d_mean + d_std, ymin=10, ymax=9990,
    #               linestyles='dotted',
    #               color=colors[i])
    #     ax.vlines(d_mean - d_std, ymin=10, ymax=9990,
    #               linestyles='dotted',
    #               color=colors[i])
    #     i += 1
    # ax.set_ylim(ylim)


def box_plot(data: pd.DataFrame):
    col_names = data.columns.to_list()
    col_names = [col_names[::2], col_names[1::2]]
    for col in range(len(col_names)):
        f = plt.figure()
        ax = f.add_subplot(111)
        d = [data[col_names[col]][c] for c in col_names[col]]
        bp = ax.boxplot(d, patch_artist=True,
                        notch='True', vert=0)
        colors = ['#0000FF', '#00FF00', '#FF0000']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(.6)
        for whisker in bp['whiskers']:
            whisker.set(color='#8B008B',
                        linewidth=1,
                        linestyle=":")
        for cap in bp['caps']:
            cap.set(color='#8B008B',
                    linewidth=0.5)
        for median in bp['medians']:
            median.set(color='red',
                       linewidth=1)
        # changing style of fliers
        for flier in bp['fliers']:
            flier.set(marker='D',
                      color='#e7298a',
                      alpha=0.5,
                      linewidth=0.5)
        labels = ['S1', 'S2', 'S3']
        ax.set_yticklabels(labels)
        # ax.set_xlim((36, 39))
        ax.set_xlabel(r'T [$^\circ$C]')
        title = 'TC' + str(col + 1)
        plt.title(title)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.grid(visible=True, which='both')
        plt.show()


def plot_mean_std(data: pd.DataFrame):
    means = data.mean()
    f, ax = plt.subplots()
    sns.despine(f)
    columns_titles = ['S1_TC1', 'S2_TC1', 'S3_TC1',
                      'S1_TC2', 'S2_TC2', 'S3_TC2']
    d1 = data.reindex(columns=columns_titles)
    for item in range(len(means)):
        sns.pointplot(d1, linestyles='None', errorbar='sd',
                      errwidth=0.5, capsize=0.1, markers='.',
                      scale=0.75, orient='v')
    ax.set_ylabel(r'T [$^\circ$C]')
    ax.set_title('Mean and standard deviation')
    ylim = ax.get_ylim()
    d = 2.5
    ax.vlines(d, ymin=ylim[0]-10, ymax=ylim[1]+10,
              linestyles='solid', colors='black')
    ax.set_ylim(ylim)
    ax.text(2, ylim[1]-0.05, 'TC 1')
    ax.text(d+0.1, ylim[1]-0.05, 'TC 2')
    ax.grid(visible=True, which='both')
    ax.set_xticklabels(['S1', 'S2', 'S3',
                        'S1', 'S2', 'S3'])


def plot_modal_values(data: pd.DataFrame):
    columns_titles = ['S1_TC1', 'S2_TC1', 'S3_TC1',
                      'S1_TC2', 'S2_TC2', 'S3_TC2']
    data = data.reindex(columns=columns_titles)
    col_names = data.columns.to_list()
    mode_counts = {}
    f, ax = plt.subplots()
    sns.despine(f)
    i = 0
    for col in range(len(col_names)):
        d1 = data[col_names[col]]
        data_mode = d1.mode()
        for mode in data_mode:
            unique, counts = np.unique(d1, return_counts=True)
            mode_counts = dict(zip(unique, counts))[mode]
            ax.scatter(i, mode)
            txt = str(mode_counts)
            ax.annotate(txt, (i+0.05, mode+0.005))
        i += 1
    ax.set_ylabel(r'T [$^\circ$C]')
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xticklabels(col_names)
    ax.set_title('Modal values')
    ylim = ax.get_ylim()
    d = 2.5
    ax.vlines(d, ymin=ylim[0]-10, ymax=ylim[1]+10,
              linestyles='solid', colors='black')
    ax.set_ylim(ylim)
    ax.text(2, ylim[1]-0.05, 'TC 1')
    ax.text(d+0.1, ylim[1]-0.05, 'TC 2')
    ax.grid(visible=True, which='both')
    ax.set_xticklabels(['S1', 'S2', 'S3',
                        'S1', 'S2', 'S3'])


# %%
# plot_data(df)
print(df.info())
df = clear_data(df)
print(df.info())
print_data_stats(df)
# %%
plot_data(df)
plot_hist(df)
box_plot(df)
plot_mean_std(df)
plot_modal_values(df)


# %%
df = clear_data(df)


def a(data: pd.DataFrame):
    columns_titles = ['S1_TC1', 'S2_TC1', 'S3_TC1',
                      'S1_TC2', 'S2_TC2', 'S3_TC2']
    data = data.reindex(columns=columns_titles)
    data = data.reset_index(inplace=False)
    data = data.rename(columns={'index': 'sample'})
    dfm = data.melt('sample', var_name='cols', value_name='T [C]')
    # fig.suptitle('')
    sns.lmplot(data=dfm, x='sample', y='T [C]', hue='cols', scatter=False,
               n_boot=10_000,
               col='cols',
               facet_kws=dict(sharex=False, sharey=False))


a(df)
# %%
