# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Kevin De Bruycker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pandas as pd
import numpy as np
import re
import math
import sys
from operator import itemgetter, attrgetter
from scipy import interpolate, constants
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools

class RelaxationExperiment:
    def __init__(self,
                 filename: str,
                 datacolumns_names: list = None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 ):

        if get_T_from != 'datacolumns_names_last' and get_T_from != 'curve_header_last_number':
            sys.exit('At the moment no other methods available to extract temperature apart from default')

        file = open(filename, 'r').read()
        self.filename = re.sub("\A(.*)\.([^.]*)\Z", "\\1", filename)
        # self.extension = re.sub("\A(.*)\.([^.]*)\Z", "\\2", filename)
        # basename = re.sub(re.sub("/", "", originals_dir) + "\\\\", "", re.sub("\A(.*)\.([^.]*)\Z", "\\1", filename))
        file_curves = re.split('Result:', re.sub('\s*\n\s*', '@@@', re.sub('\0', '', file)))
        file_header = file_curves.pop(0)
        self.project = re.sub('^.*Project:\t([^@]*)@@@.*$', '\\1', file_header)
        self.test_title = re.sub('^.*Test:\t([^@]*)@@@.*$', '\\1', file_header)

        self.datacolumns_names = datacolumns_names
        try: # Will raise error if no curves are actually detected in the file
            self.units = re.split('\t', re.sub('[\[\]]', '', re.sub('^.*Interval data:\t[^@]*@@@([^@]*)@@@.*$', '\\1', file_curves[0])))
        except:
            self.units = None

        if datacolumns_names is not None:
            curves = []
            for idx, curve in enumerate(file_curves):
                columns = re.split('\t', re.sub('^.*Interval data:\t([^@]*)@@@.*$', '\\1', curve))
                # data = [[float(number) for number in re.split('\t', line)] for line in re.split('@@@', re.sub(',', '.', re.sub('^.*Interval data:\t[^@]*@@@[^@]*@@@(.*)(@@@)+$', '\\1', curve)))]
                # data = pd.DataFrame(data, columns=columns)[retainedColumns]
                data = [re.split('\t', line) for line in
                        re.split('@@@', re.sub(',', '.', re.sub('^.*Interval data:\t[^@]*@@@[^@]*@@@(.*)(@@@)+$', '\\1', curve)))]
                data = pd.DataFrame(data, columns=columns)[datacolumns_names].apply(pd.to_numeric, errors='coerce')
                data.dropna(axis=0, how='any', inplace=True)
                if get_T_from == 'datacolumns_names_last':
                    temperature = round(data[datacolumns_names[-1]].mean())
                    data.drop(columns=[datacolumns_names[-1]], inplace=True)
                elif get_T_from == 'curve_header_last_number':
                    temperature = int(re.sub('^[^@]*\D(\d+)[^@]*@@@.*$', '\\1', curve))
                data.reset_index(drop=True, inplace=True)
                curves.append({'data': data,
                               'T': temperature,
                               'evaluate': True,
                               # 'tau': tau
                               })
            self.curves = sorted(curves, key=itemgetter('T'), reverse=True)
        else:
            self.curves = None
            print('Parameter datacolumns_names not passed to RelaxationExperiment, curves not read.')
        if T_unit is not None:
            self.T_unit = T_unit
        else:
            if '°C' in self.units:
                self.T_unit = '°C'
            else:
                sys.exit('Not sure what the temperature unit is, please provide T_unit.')

    def set_evaluated_T(self, T_min: float = None, T_max: float = None, T_range=None, T_list=None):
        if T_min == T_max == T_range == T_list is None:
            return
        if T_list is not None:
            for curve in self.curves:
                curve['evaluate'] = True if curve['T'] in T_list else False
            if hasattr(self, 'plot_data'):
                delattr(self, 'plot_data')
            return
        if T_range is not None:
            T_min = min(T_range)
            T_max = max(T_range)
        if T_min is None or T_max is None:
            sys.exit('Could not resolve the temperatures to be evaluated. Check parameters T_min, T_max, T_range or T_list.')
        else:
            for curve in self.curves:
                curve['evaluate'] = True if T_min <= curve['T'] <= T_max else False
            if hasattr(self, 'plot_data'):
                delattr(self, 'plot_data')
            return

    def get_plot_data(self):
        self.plot_data = pd.DataFrame(columns=[[],[]])
        for curve in self.curves:
            if curve['evaluate']:
                tmp = curve['data'].copy(deep=True)
                tmp.columns = [np.full(len(tmp.columns), curve['T']), list(tmp.columns)]
                self.plot_data = self.plot_data.join(tmp, how='outer')
        return self.plot_data

    def export_plot_data(self, filename=None, excel=False):
        if not hasattr(self, 'plot_data'):
            self.get_plot_data()
        if excel:
            if filename is not None:
                self.plot_data.to_excel(filename)
            else:
                self.plot_data.to_excel(self.filename + '_relaxationplot.xlsx')
        else:
            if filename is not None:
                self.plot_data.to_csv(filename, index=False)
            else:
                self.plot_data.to_csv(self.filename + '_relaxationplot.csv', index=False)

    @staticmethod
    def get_Ea(T, tau, T_unit='°C', show_plot=False, return_plot=False, plot_size: list = None, plot_dpi: float = None, return_plot_data=False):
        '''

        :param T:
        :param tau:
        :param T_unit:
        :param plot: Defines if the Arrhenius plot should be plot and shown
        :param return_plot_data:
        :type T: list or np.ndarray
        :type tau: list or np.ndarray
        :type T_unit: str
        :type plot: bool
        :type return_plot_data: bool
        :return: [Ea, std.err., R2, [ndarray(1/T), ndarray(ln(tau)), ndarray(predicted ln(tau))]]
        :rtype: list
        '''

        if type(T) == list:
            T = np.array(T)
        ln_tau = np.array([math.log(elem) for elem in tau])

        if T_unit == '°C':
            T = T + 273.15
        elif T_unit == 'K':
            pass
        else:
            sys.exit('Invalid temperature unit passed to determineEa.')
        T_inv = 1 / T
        # sklearn method does not allow to calculate std err on the linear regression
        # statsmodels method
        X = sm.add_constant(T_inv, prepend=False)
        olsResult = sm.OLS(ln_tau, X).fit()
        slope = list(zip(olsResult.params, olsResult.bse))[0]
        # intercept = list(zip(olsResult.params, olsResult.bse))[1]
        R2 = olsResult.rsquared
        ln_tau_pred = olsResult.predict()

        if show_plot or return_plot:
            fig_Ea = plt.figure(figsize=plot_size, dpi=plot_dpi)
            ax = fig_Ea.add_subplot(111)
            ax.scatter(1000 * T_inv, ln_tau)
            ax.plot(1000 * T_inv, ln_tau_pred, 'r--')
            plt.title('Arrhenius plot')
            plt.xlabel(r'1000/T (K$^{-1}$)')
            plt.ylabel(r'ln($\tau$)')
            plt.text((3 * (1000 * T_inv).min() + (1000 * T_inv).max()) * .25,
                     (ln_tau_pred.min() + 3 * ln_tau_pred.max()) * .25,
                     r'$\mathregular{E_a}$ = ' + str(round(slope[0] * constants.R / 1000, 2)) + r' $\pm$ ' + str(
                         round(slope[1] * constants.R / 1000, 2)) + r' kJ$\,$mol$^{-1}$' + '\n' + r'R$^2$ = ' + str(
                         round(R2, 4)),
                     horizontalalignment='center', verticalalignment='bottom', )
            if show_plot:
                plt.show()

        plt.close()
        results = [elem * constants.R for elem in slope] + [R2]
        if return_plot_data:
            results.append([T_inv, ln_tau, ln_tau_pred])
        if return_plot:
            results.append(fig_Ea)

        return results

    def analyse_arrhenius(self, show_plot=True, return_plot=False, plot_size: list = None, plot_dpi: float = None):
        self.arrhenius = pd.DataFrame([[curve['T'], curve['tau']] for curve in self.curves if curve['evaluate']], columns=['T', 'tau']).dropna(axis=0, how='any')
        # self.arrhenius = self.arrhenius.dropna(axis=0, how='any', inplace=True)

        tmp = self.get_Ea(T=self.arrhenius['T'].to_numpy(),
                          tau=self.arrhenius['tau'].to_numpy(),
                          T_unit=self.T_unit,
                          show_plot=show_plot,
                          return_plot=return_plot,
                          plot_size=plot_size,
                          plot_dpi=plot_dpi,
                          return_plot_data=True)
        if return_plot:
            self.arrhenius_plot = tmp[-1]
        else:
            self.arrhenius_plot = None
        self.Ea = tmp[0:3]
        self.arrhenius = self.arrhenius.join(pd.DataFrame(tmp[3], index=['T_inv', 'ln_tau', 'ln_tau_pred']).T)

    def export_arrhenius_data(self, filename=None, excel=False):
        if not hasattr(self, 'Ea'):
            self.analyse_arrhenius(show_plot=False)
        if excel:
            if filename is not None:
                self.arrhenius.to_excel(filename, index=False)
            else:
                self.arrhenius.to_excel(self.filename + '_arrheniusplot.xlsx', index=False)
        else:
            if filename is not None:
                self.arrhenius.to_csv(filename, index=False)
            else:
                self.arrhenius.to_csv(self.filename + '_arrheniusplot.csv', index=False)

class StressRelaxation(RelaxationExperiment):
    @staticmethod
    def get_tau(time, normRelaxMod, mode: str = 'interpolate_highest'):
        # Gives the time value where normRelaxMod passes the 1/e threshold. More specifically the last timepoint before
        # it drops below 1/e (or multiple in case of noisy data), which is not necessarily the timepoint closest to the
        # intersection
        if type(time) == list:
            time = np.array(time)
        if type(normRelaxMod) == list:
            normRelaxMod = np.array(normRelaxMod)
        e = np.full(len(time), 1 / math.e)
        intersections = np.argwhere(np.diff(np.sign(normRelaxMod - e))).flatten()
        if len(intersections) == 0:
            return None

        if mode == 'first_highest': # simply returns the first value of the list of the latest intersection, not taking into account the position of the 'true' intersection
            return time[intersections[-1]]
        elif mode == 'closest':  # simply gives time entry where normRelaxMod is closest to 1/e, does not take multiple intersections into account
            return float(time[np.argmin(abs(normRelaxMod - e))])
        elif mode == 'closest_highest':
            if abs(normRelaxMod[intersections[-1]] - 1 / math.e) < abs(
                    normRelaxMod[intersections[-1] + 1] - 1 / math.e):
                return time[intersections[-1]]
            else:
                return time[intersections[-1] + 1]
        elif mode == 'interpolate':
            tau = []
            for intersection in intersections:
                f = interpolate.interp1d(normRelaxMod[intersection:intersection + 2],
                                         time[intersection:intersection + 2])
                tau.append(float(f(1 / math.e)))
            if len(tau) == 1:
                return tau[0]
            else:
                return tau
        elif mode == 'interpolate_highest':
            '''
            i = -1
            while np.diff(np.sign(normRelaxMod - e))[intersections[i]] > 0:
                #make sure tangent is negative so the tau returned is the highest one where normRelaxMod drops below 1/e
                i -= 1
            '''
            f = interpolate.interp1d(normRelaxMod[intersections[-1]:intersections[-1] + 2],
                                     time[intersections[-1]:intersections[-1] + 2])
            return float(f(1 / math.e))
        else:
            sys.exit('Invalid mode passed to determineTau.')

    def __init__(self,
                 filename: str,
                 datacolumns_names=None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 T_range=None,
                 datapoints_discarded=None,
                 normalise_relax_mod=True,
                 tau_mode='interpolate_highest',
                 ):

        if datacolumns_names is None:
            if get_T_from == 'datacolumns_names_last':
                datacolumns_names = ['Time', 'Relaxation Modulus', 'Temperature']
            else:
                datacolumns_names = ['Time', 'Relaxation Modulus']

        super().__init__(filename, datacolumns_names, get_T_from, T_unit)
        self.set_evaluated_T(T_range=T_range)

        if datapoints_discarded is not None:
            if type(datapoints_discarded) == int:
                datapoints_discarded = np.full(len(self.curves), datapoints_discarded)
            elif len(datapoints_discarded) != len(self.curves):
                sys.exit('The length of the list of datapoints that should be discarded (' + str(
                    len(datapoints_discarded)) + ') is different from the number of curves to be analysed (' + str(
                    len(self.curves)) + ').')

        for idx, curve in enumerate(self.curves):
            if datapoints_discarded is not None:
                curve['data'].drop(range(0, datapoints_discarded[idx]), inplace=True) # detele certain parts from range, meant to calculate tau
                curve['data'].reset_index(drop=True, inplace=True)
            if normalise_relax_mod:
                self.normalised_relax_mod = True
                curve['data'][datacolumns_names[1]] /= curve['data'][datacolumns_names[1]].max()  # normalisation
                curve['tau'] = self.get_tau(curve['data'][datacolumns_names[0]].to_numpy(),
                                            curve['data'][datacolumns_names[1]].to_numpy(),
                                            mode=tau_mode)
            else:
                self.normalised_relax_mod = False
                # calculate tau by normalising on the fly
                curve['tau'] = self.get_tau(curve['data'][datacolumns_names[0]].to_numpy(),
                                            (curve['data'][datacolumns_names[1]] / curve['data'][datacolumns_names[1]].max()).to_numpy(),
                                            mode=tau_mode)

    def plot(self, plot_size: list = None, plot_dpi: float = None, return_plot=False):
        if not hasattr(self, 'plot_data'):
            self.get_plot_data()

        fig_relax = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_relax.add_subplot(111)
        for temp in np.flip(np.unique([col[0] for col in self.plot_data])):
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]], self.plot_data[temp, self.datacolumns_names[1]],
                    label=str(temp) + '$\,$' + self.T_unit)
        if self.normalised_relax_mod:
            tmp_array = np.array([self.plot_data[x, self.datacolumns_names[0]] for x in np.unique([col[0] for col in self.plot_data])])
            x_range = np.arange(np.nanmin(tmp_array), np.nanmax(tmp_array), (np.nanmax(tmp_array) - np.nanmin(tmp_array)) / 10)
            ax.plot(x_range, np.full(len(x_range), 1 / math.e), '--', color='grey')
            plt.ylabel(r'Normalised relaxation modulus')
        else:
            plt.ylabel(r'Relaxation modulus (Pa)')
        ax.set_xscale('log')
        ax.legend()
        plt.title('Stress relaxation')
        plt.xlabel(r'Time (s)')
        if return_plot:
            plt.close()
            return fig_relax
        else:
            plt.show()


class FrequencySweep(RelaxationExperiment):
    @staticmethod
    def get_tau(ang_freq, g_storage, g_loss, mode: str = 'interpolate_highest'):
        # Gives the time value where normRelaxMod passes the 1/e threshold. More specifically the last timepoint before
        # it drops below 1/e (or multiple in case of noisy data), which is not necessarily the timepoint closest to the
        # intersection
        if type(ang_freq) == list:
            ang_freq = np.array(ang_freq)
        if type(g_storage) == list:
            g_storage = np.array(g_storage)
        if type(g_loss) == list:
            g_loss = np.array(g_loss)
        g_diff = g_storage - g_loss
        intersections = np.argwhere(np.diff(np.sign(g_diff))).flatten()
        if len(intersections) == 0:
            return None

        if mode == 'first_highest': # simply returns the first value of the list of the latest intersection, not taking into account the position of the 'true' intersection
            return 1 / ang_freq[intersections[-1]]
        if mode == 'closest':  # simply gives time entry where normRelaxMod is closest to 1/e, does not take multiple intersections into account
            return 1 / float(ang_freq[np.argmin(abs(g_diff))])
        elif mode == 'closest_highest':
            tau_inv = []
            for intersection in intersections:
                if abs(g_diff[intersection]) < abs(g_diff[intersection + 1]):
                    tau_inv.append(ang_freq[intersection])
                else:
                    tau_inv.append(ang_freq[intersection + 1])
            return (1 / np.array(tau_inv)).max()
        elif mode == 'interpolate' or mode == 'interpolate_highest':
            tau_inv = []
            for intersection in intersections:
                f = interpolate.interp1d(g_diff[intersection:intersection + 2],
                                         ang_freq[intersection:intersection + 2])
                tau_inv.append(float(f(0)))
            if len(tau_inv) == 1:
                return 1 / tau_inv[0]
            elif mode == 'interpolate':
                return list(1 / np.array(tau_inv))
            elif mode == 'interpolate_highest':
                return (1 / np.array(tau_inv)).max()
        else:
            sys.exit('Invalid mode passed to determineTau.')

    def __init__(self,
                 filename: str,
                 datacolumns_names=None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 T_range=None,
                 datapoints_discarded=None,
                 tau_mode='interpolate_highest',
                 ):

        if datacolumns_names is None:
            if get_T_from == 'datacolumns_names_last':
                datacolumns_names = ['Angular Frequency', 'Storage Modulus', 'Loss Modulus', 'Temperature']
            else:
                datacolumns_names = ['Angular Frequency', 'Storage Modulus', 'Loss Modulus']

        super().__init__(filename, datacolumns_names, get_T_from, T_unit)
        self.set_evaluated_T(T_range=T_range)

        if datapoints_discarded is not None:
            if type(datapoints_discarded) == int:
                datapoints_discarded = np.full(len(self.curves), datapoints_discarded)
            elif len(datapoints_discarded) != len(self.curves):
                sys.exit('The length of the list of datapoints that should be discarded (' + str(
                    len(datapoints_discarded)) + ') is different from the number of curves to be analysed (' + str(
                    len(self.curves)) + ').')

        #check that the angular frequency is in rad/s, otherwise recalculation is needed
        if 'rad/s' not in self.units and 'Hz' in self.units:
            print('Assuming the frequency is given in Hz, please export as rad/s next time.')
            for curve in self.curves:
                curve['data'][datacolumns_names[0]] *= 2 * constants.pi

        for idx, curve in enumerate(self.curves):
            if datapoints_discarded is not None:
                curve['data'].drop(range(0, datapoints_discarded[idx]), inplace=True) # detele certain parts from range, meant to calculate tau
                curve['data'].reset_index(drop=True, inplace=True)
            # curve['data'][datacolumns_names[1]] /= curve['data'][datacolumns_names[1]].max()  # no normalisation
            curve['tau'] = self.get_tau(curve['data'][datacolumns_names[0]].to_numpy(),
                                        curve['data'][datacolumns_names[1]].to_numpy(),
                                        curve['data'][datacolumns_names[2]].to_numpy(),
                                        mode=tau_mode)

    def plot(self, plot_size: list = None, plot_dpi: float = None, return_plot=False):
        if not hasattr(self, 'plot_data'):
            self.get_plot_data()

        mpl_default = mpl.rcParams['axes.prop_cycle']
        mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=itertools.chain(
            *zip([color['color'] for color in mpl_default], [color['color'] for color in mpl_default])))

        fig_relax = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_relax.add_subplot(111)
        for temp in np.flip(np.unique([col[0] for col in self.plot_data])):
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]], self.plot_data[temp, self.datacolumns_names[1]],
                    '-', label=str(temp) + "$\,$°C (G')")
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]], self.plot_data[temp, self.datacolumns_names[2]],
                    '--', label=str(temp) + '$\,$°C (G")')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        plt.title('Frequency sweep')
        plt.xlabel(r'Frequency (rad$\cdot$s$^{-1}$)')
        plt.ylabel(r'Modulus (Pa)')
        mpl.rcParams['axes.prop_cycle'] = mpl_default
        if return_plot:
            plt.close()
            return fig_relax
        else:
            plt.show()
