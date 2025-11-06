import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
imports: [RouterOutlet, RouterLink, RouterLinkActive, CommonModule],
  template: `
    <div class="app-container">
      <header>
        <nav class="navbar">
          <div class="logo">
            <h1>📊 Excel Data Mapper</h1>
          </div>
          <ul class="nav-menu">
            <li><a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Inicio</a></li>
            <li class="dropdown">
              <a href="#">Funciones ▼</a>
              <ul class="dropdown-menu">
                <li><a routerLink="/autodetect">🤖 Auto-Detección</a></li>
                <li><a routerLink="/profiles">📝 Perfiles</a></li>
                <li><a routerLink="/batch">⚡ Batch</a></li>
                <li><a routerLink="/scanner">🔍 Scanner</a></li>
                <li><a routerLink="/unifier">🔗 Unificador</a></li>
                <li><a routerLink="/comparator">📊 Comparador</a></li>
                <li><a routerLink="/exporter">💾 Exportador</a></li>
              </ul>
            </li>
          </ul>
        </nav>
      </header>
      
      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
      
      <footer>
        <p>Excel Data Mapper v1.0.0 - Flask + Angular</p>
      </footer>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 0;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
      padding: 1rem 2rem;
    }

    .logo h1 {
      margin: 0;
      font-size: 1.5rem;
    }

    .nav-menu {
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      gap: 2rem;
    }

    .nav-menu a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      transition: background 0.3s;
    }

    .nav-menu a:hover,
    .nav-menu a.active {
      background: rgba(255,255,255,0.2);
    }

    .dropdown {
      position: relative;
    }

    .dropdown-menu {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      background: white;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      border-radius: 4px;
      min-width: 200px;
      list-style: none;
      padding: 0.5rem 0;
      margin-top: 0.5rem;
      z-index: 1000;
    }

    .dropdown:hover .dropdown-menu {
      display: block;
    }

    .dropdown-menu li {
      padding: 0;
    }

    .dropdown-menu a {
      color: #333;
      display: block;
      padding: 0.75rem 1rem;
    }

    .dropdown-menu a:hover {
      background: #f0f0f0;
    }

    .main-content {
      flex: 1;
      max-width: 1200px;
      margin: 2rem auto;
      padding: 0 2rem;
      width: 100%;
    }

    footer {
      background: #333;
      color: white;
      text-align: center;
      padding: 1rem;
      margin-top: auto;
    }
  `]
})
export class AppComponent {
  title = 'Excel Data Mapper';
}
