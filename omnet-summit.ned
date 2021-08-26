////
//// This program is free software: you can redistribute it and/or modify
//// it under the terms of the GNU Lesser General Public License as published by
//// the Free Software Foundation, either version 3 of the License, or
//// (at your option) any later version.
////
//// This program is distributed in the hope that it will be useful,
//// but WITHOUT ANY WARRANTY; without even the implied warranty of
//// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//// GNU Lesser General Public License for more details.
////
//// You should have received a copy of the GNU Lesser General Public License
//// along with this program.  If not, see http://www.gnu.org/licenses/.
////

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.integrated.IntegratedMultiVisualizer;
import inet.common.scenario.ScenarioManager;
import tdma.scheduler.TdmaScheduler;
import data_traffic_applications.UdpTraceBasedApp;
import inet.node.inet.INetworkNode;
import trace_based_radio.TraceBasedRadio;


network example_simulation
{
    parameters:
        int numAircrafts = default(0);
        int numGroundStations = default(1);
        string mobility_file = "NAT1515d3_data/NAT1515d3_mobility.txt";
        string scenarioManager_file = "NAT1515d3_data/NAT1515d3_scenarioManager.xml";
        @display("bgb=2400000,800000;bgl=2");
        @figure[title](type=label; pos=0,-1; anchor=sw; color=darkblue);
        @figure[rcvdPkText](type=indicatorText; pos=1110000,170000; anchor=w; font=,27000; textFormat="packets received: %g"; initialValue=0);
        @statistic[packetReceived](source=groundStation.app[0].packetReceived; record=figure(count); targetFigure=rcvdPkText);
    submodules:
        scenarioManager: ScenarioManager;
        radioMedium: <default("UnitDiskRadioMedium")> like IRadioMedium {
            @display("p=580,275");
        }

        visualizer: IntegratedMultiVisualizer {
            @display("p=100,200");
        }
        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=100,100;is=s");
        }

        scheduler: TdmaScheduler {
            parameters:
                @display("p=100,400;is=s");
        }

        aircraft[numAircrafts]: <default("WirelessHost")> like INetworkNode {
            parameters:
                @display("i=device/aircraft_west_s");
        }

        groundStation: <default("WirelessHost")> like INetworkNode {
            parameters:
                @display("p=1200000,400000;i=device/receiverdish_vl");
        }
}
