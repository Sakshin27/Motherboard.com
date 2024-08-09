import json
import os
from datetime import datetime, timedelta

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
COURSE_TITLES = {
    "BCHY101": "Chemistry",
    "BPHY101": "Physics",
    "BEEE102": "BEEE",
    "BCSE202": "DSA",
    "BCSE102": "OOPS",
    "BITE202": "DL & M",
    "BMEE201": "Mechanics",
    "BCLE201": "Constr Materials",
    "BCSE103": "Java",
    "BMAT102": "Diff Eqns",
    "BECE201": "EMD",
    "BECE203": "Circuit Theory",
    "BENG101": "English",
    "BSTS202": "QSP",
    "BHUM106": "Sociology",
    "BECE102": "DSD",
    "BENG102": "Tech Report Writing",
    "BESP101": "Spanish",
    "BHUM107": "Sustain & Society",
    "BMAT201": "Complex Variables",
    "BMAT205": "Discrete Mathematics",
    "BCLE202": "fluid",
    "BCLE203": "solids",
    "BCLE204": "surveying",
    "BCLE205": "evm",
    "BCLE209": "geology",
    "BCSE203": "Web programming",
    "BCSE204": "Design and analysis algorithms",
    "BCSE205": "Computer architecture and organisation",
    "BCSE304": "theory of computation",
    "BECE204": "Microprocessor and microcontrollers",
    "BMAT202": "Probability and statistics",
    "BSTS102": "quantitative skills practice II",
    "BMEE204": "Fluid Mechanics and Machine",
    "BMEE207": "Kinematics and Dynamics of Machines", 
    "BMEE215": "Engineering Optimization", 
    "BMEE302": "Metal Casting and Welding", 
    "BSSC101": "Essence of Traditional Knowledge", 
    "BECE206": "Analog Circuits Theory",
    "BECE207": "Random processes",
    "BECE301": "Digital signal processing theory",
    "BEEE208": "Analog Electronics",
    "BEEE211": "VLSI Design",
    "BEEE215": "DC Machines and Transformers",
    "BEEE301": "Power Electronics",
    "BHUM220": "Financial Institutions and Markets",
    "BMT1011": "Business Law",
    "BMT1022": "Total Quality Management",
    "BMT2003": "Organizational Change and Development",
    "BMT2005": "Sales Management",
    "BMT2006": "Services Marketing",
    "BMT2019": "Performance Management",
    "BMT3002": "Entrepreneurship",
    "ENG1913": "Effective Communication Skills",
    "HUM1032": "Ethics and Values",
    "STS2012": "Aptitude and Reasoning Skills",
    "MOC2437": "Conservation Economics",
    "CCA1708": "Export Marketing",
    "BMT1013": "Banking and Insurance",
    "BMT1014": "Managing Personal Finance",
    "BMT1016": "Stress Management",
    "BMT2008": "Advertising Management",
    "BMT2009": "Retail Management",
    "BMT2011": "Training and Development",
    "BMT3010": "Fintech",
    "STS3003": "Preparedness for Recruitment",
    "CCA2707": "Cost Accounting",
    "CCA2708": "Banking Theory and Practice",
    "CCA2714": "Service Marketing",
    "CCA3701": "Income Tax Law and Practice",
    "CCA3704": "Advanced Financial Management",
    "CCA3705": "Advanced Performance Management",
    "STS3003": "Preparedness for Recruitment",
    "BMEE210": "Mechatronics and Measurement Systems",
    "BMEE301": "Design of Machine Elements",
    "BMEE303": "Thermal Engineering Systems",
    "BMEE304": "Metal Forming and Machining",
    "BMEE327": "Vehicle Dynamics",
    "BMEE355": "Cloud Computing using Salesforce",
    "BSTS301": "Advanced Competitive Coding - I",
    "BCSE302": "Database Systems",
    "BCSE303": "Operating Systems",
    "BCSE306": "Artificial Intelligence",
    "BCSE308": "Computer Networks",
    "BCSE355": "AAWS Solutions Architect",    
    "BAG1002": "Micro propagation Technologies",    
    "BAG2003": "Manures, Fertilizers and Soil Fertility Management", 
    "BAG2004": "Crop Improvement - I",   
    "BAG2006": "Pests of Crops and Stored Grains and their Management",    
    "BAG2007": "Diseases of Field and Horticultural Crops and their Management - I",    
    "BAG3001": "Principles of Integrated Pests and Disease Management",    
    "BAG3004": "Geoinformatics, Nanotechnology and Precision Farming",    
    "BAG4001": "Agribusiness Management",    
    "MGT1053": "Entrepreneurship Development, Business Communication and IPR",
    "UCCA202L": "Corporate Law",  
    "UCCA203L": "Financial Management",
    "UCCA209L": "Banking Theory and Practice",
    "UCCA231L": "Digital Marketing for Financial Services",
    "UCCA236L": "Fintech Intelligence",
    "UCCA316E": "Stock Market Operations",
    "UCSC326E": "Data Analysis with Python",
}


def timings_to_datetimes(start, end):
    date = datetime(2022, 9, 19, 0, 0, 0, 0)
    start = date.replace(**dict(zip(("hour", "minute"), map(int, start.split(":")))))
    end = date.replace(**dict(zip(("hour", "minute"), map(int, end.split(":")))))
    return start, end


file_list = [file for file in os.listdir() if ".txt" in file]

for file in file_list:
    # Directly copied input from VTOP
    name = file[:-4]
    print(f"Processing {name}")

    inp = open(f"{name}.txt").read()

    # Organise input into lists
    data = [line.split("\t") for line in inp.split("\n") if line]

    # Remove 'Start', 'End', 'LAB', 'THEORY' and day names
    for i, line in enumerate(data):
        if line[1].isalpha():
            data[i] = line[2:]
        else:
            data[i] = line[1:]

    # Seperate out timings for theory and lab
    theory_timings = data[:2]
    lab_timings = data[2:4]
    data = data[4:]

    # Store each day's classes in that day's list
    timetable = [[] for _ in range(7)]
    for d, line in enumerate(data):
        for i, slot in enumerate(line):
            if slot != "-" and "-" in slot:
                # Every second line is a lab entry
                if d % 2 == 1:
                    start, end = timings_to_datetimes(
                        lab_timings[0][i], lab_timings[1][i]
                    )
                    if timetable[d // 2]:
                        if abs(start - timetable[d // 2][-1]["end"]) <= timedelta(
                            minutes=2
                        ):
                            timetable[d // 2][-1]["end"] = end
                            continue
                else:
                    start, end = timings_to_datetimes(
                        theory_timings[0][i], theory_timings[1][i]
                    )

                slot = slot.split("-")
                slot[1] = slot[1][:-1]

                course_title = COURSE_TITLES.get(slot[1], slot[1])

                # Every second line is a lab entry
                course_title += " Lab" if d % 2 == 1 else ""

                period = {
                    "title": course_title,
                    "venue": slot[3],
                    "start": start,
                    "end": end,
                }
                timetable[d // 2].append(period)

    timetable = [sorted(day, key=lambda x: x["start"]) for day in timetable]

    for day in timetable:
        for period in day:
            period["timings"] = [
                period["start"].hour,
                period["start"].minute,
                period["end"].hour,
                period["end"].minute,
            ]
            del period["start"]
            del period["end"]

    json.dump(timetable, open(f"../{name}.json", "w"), indent="\t")

    print(f"{name}.json created successfully.")
