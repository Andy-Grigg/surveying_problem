import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('results/results_all_methods_sparse.pkl')
df.drop(['Number of Wells', 'Number of Sites'], axis=1, inplace=True)
ax = df.plot.bar()
ax.set_xlabel(None)
ax.set_ylabel("Execution time / s")
ax.set_xticklabels([f"Size: {grid_size}\n"
                    f"Threshold: {threshold}" for (grid_size, threshold), _ in df.iterrows()])
ax.set_yscale('log')
plt.xticks(rotation=0)
plt.show()

df = pd.read_pickle('results/results.pkl')
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.float_format', '{:.3e}'.format):
    print(df)
df.rename(columns={'Number of Sites': 'number_of_sites',
                   'Number of Wells': 'number_of_wells',
                   'Recursive Method': 'recursive',
                   'Stack Method (List)': 'stack_list',
                   'Stack Method (deque)': 'stack_deque'},
          inplace=True)
df['average_well_size'] = df.apply(lambda row:
                                       row.number_of_sites/row.number_of_wells
                                       if row.number_of_wells != 0 else 0,
                                   axis=1)
df['stack_div_recursive'] = df.apply(lambda row: row.stack_list/row.recursive, axis=1)
df['list_div_deque'] = df.apply(lambda row: row.stack_list/row.stack_deque, axis=1)

# Average well size vs Probability
df_well_size = df.drop(['recursive',
                        'stack_list',
                        'stack_deque',
                        'stack_div_recursive',
                        'list_div_deque',
                        'number_of_sites',
                        'number_of_wells'],
                       axis=1)

ax = df_well_size.unstack(level=0).plot()
ax.set_xlabel('Probability threshold')
ax.set_ylabel('Average well size')
ax.legend([10, 50, 100, 500, 1000, 5000, 10000], title = 'Grid size', fancybox=True)
plt.show()


# Different Methods
df_recursive_vs_stack = df.drop(['number_of_sites',
                        'number_of_wells',
                        'average_well_size',
                        'stack_div_recursive',
                        'list_div_deque'],
                       axis=1)

# Recursive vs Stack
df_recursive_vs_stack = df.drop(['number_of_sites',
                        'number_of_wells',
                        'average_well_size',
                        'stack_div_recursive',
                        'list_div_deque'],
                       axis=1)

columns = ['recursive', 'stack_list']
df_recursive_vs_stack_size_high = df_recursive_vs_stack.loc[pd.IndexSlice[:, 0.99], columns]
df_recursive_vs_stack_size_low = df_recursive_vs_stack.loc[pd.IndexSlice[:, 0.7], columns]
df_recursive_vs_stack_prob_big = df_recursive_vs_stack.loc[pd.IndexSlice[10000, :], columns]
df_recursive_vs_stack_prob_small = df_recursive_vs_stack.loc[pd.IndexSlice[10, :], columns]

df_recursive_vs_stack_size_high.index = df_recursive_vs_stack_size_high.index.droplevel(1)
df_recursive_vs_stack_size_low.index = df_recursive_vs_stack_size_low.index.droplevel(1)
df_recursive_vs_stack_prob_big.index = df_recursive_vs_stack_prob_big.index.droplevel(0)
df_recursive_vs_stack_prob_small.index = df_recursive_vs_stack_prob_small.index.droplevel(0)

fig, ax = plt.subplots(nrows=1, ncols=2, sharey='all', figsize=(10,6))

df_recursive_vs_stack_size_high.plot(ax=ax[0], title='Variable grid size')
df_recursive_vs_stack_size_low.plot(ax=ax[0])

ax[0].set_yscale('log')
ax[0].set_ylabel('Execution time / s')

ax[0].legend(labels = ['Recusive Method: Threshold = 0.99', 'Stack Method: Threshold = 0.99',
                     'Recusive Method: Threshold = 0.7', 'Stack Method: Threshold = 0.7'])

df_recursive_vs_stack_prob_big.plot(ax=ax[1], title='Variable probability threshold')
df_recursive_vs_stack_prob_small.plot(ax=ax[1])

ax[1].legend(labels = ['Recusive Method: Grid Size = 10,000', 'Stack Method: Grid Size = 10,000',
                     'Recusive Method: Grid Size = 10', 'Stack Method: Grid Size = 10'])
plt.show()


# List vs Deque
df_list_vs_deque = df.drop(['number_of_sites',
                        'number_of_wells',
                        'average_well_size',
                        'stack_div_recursive',
                        'list_div_deque'],
                       axis=1)

columns = ['stack_deque', 'stack_list']
df_list_vs_deque_size_high = df_list_vs_deque.loc[pd.IndexSlice[:, 0.99], columns]
df_list_vs_deque_size_low = df_list_vs_deque.loc[pd.IndexSlice[:, 0.7], columns]
df_list_vs_deque_prob_big = df_list_vs_deque.loc[pd.IndexSlice[10000, :], columns]
df_list_vs_deque_prob_small = df_list_vs_deque.loc[pd.IndexSlice[10, :], columns]

df_list_vs_deque_size_high.index = df_list_vs_deque_size_high.index.droplevel(1)
df_list_vs_deque_size_low.index = df_list_vs_deque_size_low.index.droplevel(1)
df_list_vs_deque_prob_big.index = df_list_vs_deque_prob_big.index.droplevel(0)
df_list_vs_deque_prob_small.index = df_list_vs_deque_prob_small.index.droplevel(0)

_, ax = plt.subplots(nrows=1, ncols=2, sharey='all', figsize=(10,6))

df_list_vs_deque_size_high.plot(ax=ax[0], title='Dependence of grid size on execution time')
df_list_vs_deque_size_low.plot(ax=ax[0])

ax[0].set_yscale('log')
ax[0].set_ylabel('Execution time / s')

ax[0].legend(labels = ['Deque Implementation: Threshold = 0.99',
                       'List Implementation: Threshold = 0.99',
                       'Deque Implementation: Threshold = 0.7',
                       'List Implementation: Threshold = 0.7'])


df_list_vs_deque_prob_big.plot(ax=ax[1],
                               title='Dependence of probability threshold on execution time')
df_list_vs_deque_prob_small.plot(ax=ax[1])

ax[1].legend(labels = ['Deque Implementation: Grid Size = 10,000',
                       'List Implementation: Grid Size = 10,000',
                       'Deque Implementation: Grid Size = 10',
                       'List Implementation: Grid Size = 10'])

plt.show()
