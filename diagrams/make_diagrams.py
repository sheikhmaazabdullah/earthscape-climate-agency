"""Generate all report diagrams with matplotlib (no external tools needed)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import pathlib
OUT=pathlib.Path(__file__).parent
def box(ax,x,y,w,h,text,fc="#dceeff",fs=9,shape="round"):
    if shape=="round":
        p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.06,rounding_size=0.12",fc=fc,ec="#22577a",lw=1.4)
    elif shape=="diamond":
        p=plt.Polygon([[x,y+h/2],[x+w/2,y],[x,y-h/2],[x-w/2,y]],closed=True,fc=fc,ec="#22577a",lw=1.4)
    elif shape=="cyl":
        p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.3",fc=fc,ec="#22577a",lw=1.4)
    else:
        p=Rectangle((x-w/2,y-h/2),w,h,fc=fc,ec="#22577a",lw=1.4)
    ax.add_patch(p); ax.text(x,y,text,ha="center",va="center",fontsize=fs,wrap=True)
def arrow(ax,x1,y1,x2,y2,text=""):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="->",mutation_scale=13,color="#333",lw=1.2))
    if text: ax.text((x1+x2)/2+0.08,(y1+y2)/2,text,fontsize=7.5,color="#555")
def canvas(w=11,h=7):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,10); ax.set_ylim(0,10*h/w+2); ax.axis("off"); return fig,ax
def save(fig,name,title):
    fig.suptitle(title,fontsize=13,weight="bold"); fig.tight_layout(); fig.savefig(OUT/name,dpi=150,bbox_inches="tight"); plt.close(fig); print("wrote",name)

# 1. Architecture
fig,ax=canvas()
layers=[("DATA SOURCES\nOpen-Meteo API - CSV / JSON files - Sensor stream simulator - Satellite-derived CO2 data","#ffe8cc"),
("INGESTION & VALIDATION\nSchema check - Missing-data handling (station median) - Format conversion","#dceeff"),
("STORAGE\nPartitioned files (HDFS layout: year / month / station) - SQLite database - MongoDB (optional)","#e2f0d9"),
("PROCESSING\nHadoop Streaming MapReduce (batch) - Rolling stream processor (real-time) - ML: anomaly / forecast / correlation","#fce4ec"),
("PRESENTATION & ACTION\nStreamlit dashboard (RBAC login) - Tableau views - Threshold alerts - Feedback / Support","#e8daef")]
y=8.6
for t,c in layers:
    box(ax,5,y,8.6,1.25,t,fc=c,fs=9.5)
    if y<8.6: arrow(ax,5,y+1.05,5,y+0.65)
    y-=1.55
save(fig,"01_architecture.png","EarthScape Climate Agency - System Architecture")

# 2. DFD Level 0
fig,ax=canvas(10,6)
box(ax,1.6,4.2,2.2,1.1,"Weather Stations\nSatellites / Sensors",fc="#ffe8cc")
box(ax,5,4.2,2.6,1.5,"0.0\nEarthScape Climate\nData Platform",fc="#dceeff")
box(ax,8.6,5.6,2.0,1.0,"Analysts /\nAdministrators",fc="#e2f0d9")
box(ax,8.6,2.7,2.0,1.0,"Stakeholders",fc="#e2f0d9")
arrow(ax,2.7,4.6,3.7,4.6,"climate data"); arrow(ax,6.3,4.7,7.6,5.4,"dashboards / reports")
arrow(ax,6.3,3.8,7.6,3.0,"alerts")
save(fig,"02_dfd_level0.png","Data Flow Diagram - Level 0 (Context Diagram)")

# 3. DFD Level 1
fig,ax=canvas(11,7.5)
procs=[(2,7.6,"1.0 Ingest &\nValidate Data"),(5,7.6,"2.0 Store &\nPartition Data"),(8,7.6,"3.0 Process Data\n(MapReduce / Stream)"),
       (2,3.6,"4.0 Analyse (ML)\nAnomaly / Forecast"),(5,3.6,"5.0 Visualise\nDashboard / Tableau"),(8,3.6,"6.0 Alert &\nSupport")]
for x,y,t in procs: box(ax,x,y,2.3,1.2,t,fc="#dceeff",fs=8.5)
box(ax,5,5.55,3.2,0.85,"D1: Climate Data Store (Partitioned / DB)",fc="#fff2cc",fs=8.5)
arrow(ax,3.15,7.6,3.85,7.6); arrow(ax,6.15,7.6,6.85,7.6)
arrow(ax,8,6.95,6.6,6.05); arrow(ax,3.6,5.2,2.4,4.3); arrow(ax,5,5.1,5,4.25)
arrow(ax,3.15,3.6,3.85,3.6); arrow(ax,6.15,3.6,6.85,3.6)
save(fig,"03_dfd_level1.png","Data Flow Diagram - Level 1")

# 4. Flowchart
fig,ax=canvas(8,11)
steps=[("START", "round","#e2f0d9"),("Login - check role\n(Admin / Analyst / Viewer)","rect","#dceeff"),
("Ingest data\n(CSV / JSON / API / Stream)","rect","#dceeff"),("Data valid?","diamond","#ffe8cc"),
("Handle missing values\n(station median)","rect","#fff2cc"),("Store partitioned\n(year / month / station)","rect","#dceeff"),
("Run MapReduce +\nML analysis","rect","#dceeff"),("Threshold crossed?","diamond","#ffe8cc"),
("Raise ALERT","rect","#fce4ec"),("Show dashboard /\nforecast / correlations","rect","#e8daef"),("END","round","#e2f0d9")]
y=11.4
for label,shape,c in steps:
    box(ax,4,y,3.4,0.95 if shape!="diamond" else 1.25,label,fc=c,fs=8.5,shape=shape)
    if y<11.4: arrow(ax,4,y+0.85,4,y+0.5)
    if label=="Data valid?": ax.text(6.1,y,"No -> fix / impute",fontsize=8,color="#a00")
    if label=="Threshold crossed?": ax.text(6.1,y,"No -> dashboard only",fontsize=8,color="#555")
    y-=1.15
save(fig,"04_flowchart.png","System Flowchart")

# 5. ER Diagram
fig,ax=canvas(11,7)
ents=[(2,6.8,"USERS\nuser_id (PK)\nusername, password_hash\nrole"),(5.2,6.8,"STATIONS\nstation_id (PK)\nname, latitude, longitude"),
(8.4,6.8,"CLIMATE_RECORDS\nrecord_id (PK)\nstation_id (FK), date\ntemperature, rainfall\nhumidity, co2, source"),
(2,2.8,"ALERTS\nalert_id (PK)\nrecord_id (FK)\ntype, message, created_at"),(5.2,2.8,"PREDICTIONS\nprediction_id (PK)\nstation_id (FK), date\npredicted_temp"),
(8.4,2.8,"SUPPORT_TICKETS\nticket_id (PK)\nuser_id (FK)\nmessage, status")]
for x,y,t in ents: box(ax,x,y,2.5,1.7,t,fc="#dceeff",fs=8)
arrow(ax,3.3,6.8,3.9,6.8); arrow(ax,6.5,6.8,7.1,6.8)
ax.text(5,5.7,"1 station -> many records",fontsize=8,ha="center")
arrow(ax,7.6,5.9,4.5,3.8); arrow(ax,6.5,5.9,5.6,3.7); arrow(ax,2.4,5.9,2.2,3.7)
save(fig,"05_er_diagram.png","Entity Relationship Diagram")

# 6. Use Case
fig,ax=canvas(11,7)
ax.add_patch(Rectangle((3.2,0.7),4.6,7.6,fill=False,ec="#22577a",lw=1.6)); ax.text(5.5,8.0,"EarthScape System",ha="center",fontsize=10,weight="bold")
cases=[(5.5,7.2,"Login / Logout"),(5.5,6.2,"Ingest Climate Data"),(5.5,5.2,"Run MapReduce & ML Analysis"),(5.5,4.2,"View Dashboard & Forecasts"),(5.5,3.2,"View / Configure Alerts"),(5.5,2.2,"Submit Support Ticket"),(5.5,1.2,"Manage Users (Admin)")]
for x,y,t in cases:
    ax.add_patch(plt.Circle((x,y),0.42,color="#dceeff",ec="#22577a")); 
    from matplotlib.patches import Ellipse; ax.add_patch(Ellipse((x,y),3.0,0.8,fc="#dceeff",ec="#22577a")); ax.text(x,y,t,ha="center",va="center",fontsize=8.5)
for name,x,y,ys in [("Admin",1.3,6.5,[7.2,6.2,3.2,1.2]),("Analyst",1.3,3.2,[6.2,5.2,4.2,3.2]),("Viewer / Stakeholder",8.9,4.5,[4.2,3.2,2.2])]:
    ax.text(x,y,name,ha="center",fontsize=10,weight="bold")
    for yy in ys: arrow(ax,x+ (0.9 if x<5 else -1.1),y, 4.0 if x<5 else 7.0, yy)
save(fig,"06_use_case.png","Use Case Diagram")
print("ALL DIAGRAMS DONE")
