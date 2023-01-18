import pandas as pd
import matplotlib.pyplot as plt
import statistics
import seaborn as sns


def check_bots_df(df_path: str = 'test_data.tsv', A=False, B=False, C=False):  # pd.core.frame.DataFrame
    """A- return dictionaries , B- return users df, C- return bot df"""
    df = pd.read_table(df_path)

    # 23581
    k = [0]
    for i in range(len(df['t']) - 1):
        if (abs(df['t'][i] - df['t'][i + 1]) > 21600 and df['user'][i] == df['user'][i + 1]) \
                or abs(df['t'][i] - df['t'][i + 1]) < 3:
            k.append(1)
        else:
            k.append(0)

    df2 = df.assign(susp=k)
    df3 = df2[df2['susp'] > 0]
    cnethash_list_s = df3['cnethash'].values.tolist()

    susp_df1 = df[df['cnethash'].isin(df3['cnethash'])]
    susp_df2 = df[df['user'].isin(df3['user'])]
    new_df = susp_df1.merge(susp_df2)

    # check for multiply clicks
    freq_click = []
    for h in df['user'].unique():
        hlp1 = df.loc[df['user'] == h]  # ['tn']
        if sum([q for q in hlp1['tn']]) > 2:
            freq_click.append(h)
        else:
            continue

    newer_df = new_df['user'].append(pd.Series(freq_click))

    uniq_df_susp = newer_df.unique()
    suspects_df = df[df['user'].isin(uniq_df_susp)]
    clean_df = df[~df['user'].isin(uniq_df_susp)]

    dic = {}
    dic_freq = {}
    dic_clean = {}

    # form susp_user_list according to mode time of br displaying('t)

    for i in suspects_df['user'].unique():
        vsp1 = suspects_df.loc[suspects_df['user'].isin([i])]['t']
        ls1 = [k for k in vsp1]
        oio = []
        for s in range(len(ls1) - 1):
            oio.append(abs(ls1[s + 1] - ls1[s]))
            dic[f'{i}'] = round(statistics.harmonic_mean(oio))

    # form susp_user_list according to mode time of br displaying freq(event count) ???

    """
    freq_susp=[]
    for p in suspects_df['user'].value_counts():
        if p>11:
            freq_susp.append(p)
    
    lst_susp_freq=[]
    for k in suspects_df['user'].value_counts().index[:len(freq_susp)]:
        lst_susp_freq.append(k)"""

    # form susp_user_list according to mode time of br displaying freq(event count)
    """
    for i in suspects_df['user']:
        vsp2 = suspects_df.loc[suspects_df['user'].isin([i])]['t']   #rslt_df = df[df['tn'] > 0]
        #vsp2 = vsp2[vsp2['user'].value_counts()>10]
        ls2 = [k for k in vsp2]
        oio2=[]
        for s in range(len(ls2)-1):
            oio2.append(abs(ls2[s + 1] - ls2[s]))
            dic_freq[f'{i}']= round(statistics.harmonic_mean(oio2))
        #else:
        #    continue
    """

    # form clean_user_list according to mode time

    for i in clean_df['user'].unique():
        vsp3 = clean_df.loc[clean_df['user'].isin([i])]['t']
        ls3 = [k for k in vsp3]
        oio3 = []
        for s in range(len(ls3) - 1):
            oio3.append(abs(ls3[s + 1] - ls3[s]))
            dic_clean[f'{i}'] = round(statistics.harmonic_mean(oio3))

    two_classes = []
    two_classes.append(dic)
    two_classes.append(dic_clean)

    if A:
        return two_classes
    elif B:
        return clean_df
    elif C:
        return suspects_df
    else:
        pass


#check_bots_df(A=True)


def draw_statistics(A=False, B=False, C=False):
    """A- plot differences , B- plot shows/CTR users, B- plot shows/CTR bots"""

    if A:
        lst33 = check_bots_df(A=True)
        groups = ['Bot suspicious', 'Users']
        values = [statistics.harmonic_mean(lst33[0].values()),
                  round(statistics.harmonic_mean(lst33[1].values()))]
        fig = plt.figure(figsize=(10, 5))
        plt.bar(groups, values, color='maroon',
                width=0.4)

        plt.xlabel("Groups")
        plt.ylabel("Harmonic mean of browser exposition")
        plt.title("Differences between users and bots by time of browser exposition")
        #plt.show()

        return fig

    elif B:
        cl_d = check_bots_df(B=True)
        groups = ['Shows', 'Clicks', 'CTR %', 'shows per user ratio %']
        values = [len(cl_d['tn']),
                  cl_d['tn'].value_counts()[1],
                  round(cl_d['tn'].value_counts()[1] / (len(cl_d['tn'])) * 100, 2),
                  round(len(cl_d['tn']) / (len(cl_d['user'].unique())) * 100, 2)]

        fig, ax = plt.subplots(figsize=(10, 5))
        barchart = sns.barplot(x=groups, y=values, ax=ax)
        barchart.set(title='Users')
        barchart.set(xlabel='Groups', ylabel='Clicks')
        barchart.bar_label(ax.containers[0], label_type='edge', padding=15)

        return barchart

    elif C:
        cl_s = check_bots_df(C=True)
        groups = ['Shows', 'Clicks', 'CTR %', 'shows per user ratio %']
        values = [len(cl_s['tn']),
                  cl_s['tn'].value_counts()[1],
                  round(cl_s['tn'].value_counts()[1] / (len(cl_s['tn'])) * 100, 2),
                  round(len(cl_s['tn']) / (len(cl_s['user'].unique())) * 100, 2)]

        fig, ax = plt.subplots(figsize=(10, 5))
        barchart = sns.barplot(x=groups, y=values, ax=ax)
        barchart.set(title='Bots')
        barchart.set(xlabel='Groups', ylabel='Clicks')
        barchart.bar_label(ax.containers[0], label_type='edge', padding=15)

        return barchart

draw_statistics(C=True)