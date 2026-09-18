import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Patients from "./pages/Patients";
import Documents from "./pages/Documents";
import Timeline from "./pages/Timeline";
import Events from "./pages/Events";
import Conflicts from "./pages/Conflicts";
import WhatChanged from "./pages/WhatChanged";
import Evidence from "./pages/Evidence";
import QA from "./pages/QA";
import Settings from "./pages/Settings";

type Page =
  | "Dashboard"
  | "Patients"
  | "Documents"
  | "Timeline"
  | "Events"
  | "Conflicts"
  | "What Changed"
  | "Evidence"
  | "Q&A"
  | "Settings";

function App() {
  const [page, setPage] = useState<Page>("Dashboard");

  const goToDocuments = () => {
    setPage("Documents");
  };
  const renderPage = () => {
    switch (page) {
      case "Dashboard":
        return <Dashboard />;
      case "Patients":
        return <Patients />;
      case "Documents":
        return <Documents />;
      case "Timeline":
        return <Timeline />;
      case "Events":
        return <Events />;
      case "Conflicts":
        return <Conflicts />;
      case "What Changed":
        return <WhatChanged />;
      case "Evidence":
        return <Evidence />;
      case "Q&A":
        return <QA />;
      case "Settings":
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  const menuItems: Page[] = [
    "Dashboard",
    "Patients",
    "Documents",
    "Timeline",
    "Events",
    "Conflicts",
    "What Changed",
    "Evidence",
    "Q&A",
    "Settings",
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✚</div>
          <div>
            <h1>ChronoMed</h1>
            <span>Medical Intelligence</span>
          </div>
        </div>

        <nav>
          {menuItems.map((item) => (
            <button
              key={item}
              className={page === item ? "nav-item active" : "nav-item"}
              onClick={() => setPage(item)}
            >
              <span>
                {item === "Dashboard" && "⌂"}
                {item === "Patients" && "♙"}
                {item === "Documents" && "▤"}
                {item === "Timeline" && "◷"}
                {item === "Events" && "●"}
                {item === "Conflicts" && "⚠"}
                {item === "What Changed" && "↕"}
                {item === "Evidence" && "▣"}
                {item === "Q&A" && "?"}
                {item === "Settings" && "⚙"}
              </span>
              {item}
            </button>
          ))}
        </nav>

        <div className="system-status">
          <div className="status-dot"></div>
          <div>
            <strong>System Online</strong>
            <small>AI services ready</small>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">ChronoMed /</span>
            <strong>{page}</strong>
          </div>

          <div className="topbar-right">
            <span className="demo-badge">DEMO MODE</span>
            <div className="user-avatar">KM</div>
          </div>
        </header>

        <section className="page-content">{renderPage()}</section>
      </main>
    </div>
  );
}

export default App;