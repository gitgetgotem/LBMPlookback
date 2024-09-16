import React, { useState } from 'react';

const Dropdowns = ({ onUpdate }) => {
    // Static values
    const zones = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'hq', 'i', 'j', 'k', 'npx', 'oh', 'pjm'];
    const curves = [
    'Angel_Road', 'County_Road_14', 'Day_Hollow_Road', 'FT_20_Binghmtn',
    'FT_20_Syracuse', 'FT_30_Binghmtn', 'FT_30_Syracuse', 'Hanover_Rd',
    'Harris_Road', 'Howell_Road', 'Jericho_Hill_Road', 'Kirkland',
    'National_Grid_Zone_E', 'Route_5_and_20', 'Route_64N', 'SAT_EW_Binghmtn',
    'SAT_EW_Syracuse', 'SAT_NS_Binghmtn', 'SAT_NS_Syracuse', 'Scudder_Road',
    'South_Main_St_1', 'South_Main_St_2', 'State_Hgwy_17_Hancock',
    'State_Highway_17C', 'Weaver_Rd_Rosa'
];
    const utilities = ['NYSEG', 'ORU', 'NG'];

    const [selectedZone, setSelectedZone] = useState(zones[0]);
    const [selectedCurve, setSelectedCurve] = useState(curves[0]);
    const [selectedUtility, setSelectedUtility] = useState(utilities[0]);

    const handleSubmit = () => {
        // Call the passed onUpdate function with the selected values
        onUpdate(selectedZone, selectedCurve, selectedUtility);
    };

    return (
        <div>
            <h2>Select Zone</h2>
            <select onChange={(e) => setSelectedZone(e.target.value)} value={selectedZone}>
                {zones.map(zone => (
                    <option key={zone} value={zone}>{zone}</option>
                ))}
            </select>

            <h2>Select Curve</h2>
            <select onChange={(e) => setSelectedCurve(e.target.value)} value={selectedCurve}>
                {curves.map(curve => (
                    <option key={curve} value={curve}>{curve}</option>
                ))}
            </select>

            <h2>Select Utility</h2>
            <select onChange={(e) => setSelectedUtility(e.target.value)} value={selectedUtility}>
                {utilities.map(utility => (
                    <option key={utility} value={utility}>{utility}</option>
                ))}
            </select>

            <button onClick={handleSubmit}>Run Program</button>
        </div>
    );
};

export default Dropdowns;
