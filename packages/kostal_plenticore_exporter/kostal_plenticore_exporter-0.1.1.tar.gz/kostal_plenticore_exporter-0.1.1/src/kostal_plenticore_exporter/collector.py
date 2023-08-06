import kostalplenticore
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily, InfoMetricFamily


class PlenticoreCollector:
    def __init__(self, ip: str, password: str):
        self.source = kostalplenticore.connect(ip, password)
        self.source.login()

    def _get_processdata(self, moduleid, processdata):
        return {result['id']: result['value'] for result in self.source.getProcessdata(moduleid, processdata)}

    def _info_metric(self):
        info = InfoMetricFamily('kostal_plenticore', 'Inverter metadata')
        info.add_metric([], self.source.getInfo())
        return info

    def _battery_metrics(self):
        battery_data = self._get_processdata('devices:local:battery', [
            'BatManufacturer', 'BatModel', 'BatVersionFW', 'Cycles', 'SoC'
        ])

        cycles = GaugeMetricFamily('kostal_plenticore_battery_cycles_total', "Battery cycle count")
        cycles.add_metric([], battery_data['Cycles'])

        charge = GaugeMetricFamily('kostal_plenticore_battery_charge_percent', "Battery charge in percent")
        charge.add_metric([], battery_data['SoC'])

        return (cycles, charge)

    def _event_metrics(self):
        event_data = self._get_processdata('scb:event', ['Event:ActiveErrorCnt', 'Event:ActiveWarningCnt'])

        events = GaugeMetricFamily('kostal_plenticore_active_events_total', "Active events", labels=['severity'])
        events.add_metric(["error"], event_data['Event:ActiveErrorCnt'])
        events.add_metric(["warning"], event_data['Event:ActiveWarningCnt'])

        return events

    def _energy_metrics(self):
        energy_flows = [
            'ChargeGrid', 'ChargeInvIn', 'ChargePv', 'Discharge', 'DischargeGrid',
            'Home', 'HomeBat', 'HomeGrid', 'HomeOwn', 'HomePv',
            'Pv1', 'Pv2', 'Pv3',
        ]

        energy_data = self._get_processdata('scb:statistic:EnergyFlow', [
            f'Statistic:Energy{flow}:Total' for flow in energy_flows
        ] + ['Statistic:Yield:Total'])

        metric = CounterMetricFamily(
            'kostal_plenticore_energy_flow_watt_hours', 'Total energy flows in watt hours', labels=['flow']
        )
        for flow in energy_flows:
            metric.add_metric([flow], energy_data[f'Statistic:Energy{flow}:Total'])
        metric.add_metric(['Yield'], energy_data['Statistic:Yield:Total'])
        return metric

    def collect(self):
        yield self._info_metric()
        for metric in self._battery_metrics():
            yield metric
        yield self._event_metrics()
        yield self._energy_metrics()
