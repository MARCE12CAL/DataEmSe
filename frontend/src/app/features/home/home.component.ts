import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  features = [
    {
      icon: '',
      title: 'Auto-Detección',
      description: 'Detecta automáticamente campos en archivos Excel',
      link: '/autodetect'
    },
    {
      icon: '',
      title: 'Gestión de Perfiles',
      description: 'Crea y administra perfiles de mapeo de datos',
      link: '/profiles'
    },
    {
      icon: '',
      title: 'Procesamiento Batch',
      description: 'Procesa múltiples archivos automáticamente',
      link: '/batch'
    },
    {
      icon: '',
      title: 'Scanner',
      description: 'Escanea carpetas en busca de archivos Excel',
      link: '/scanner'
    },
    {
      icon: '',
      title: 'Unificador',
      description: 'Combina múltiples archivos en uno solo',
      link: '/unifier'
    },
    {
      icon: '',
      title: 'Comparador',
      description: 'Compara archivos contra modelos',
      link: '/comparator'
    },
    {
      icon: '',
      title: 'Exportador',
      description: 'Exporta a CSV, JSON, SQL y más',
      link: '/exporter'
    }
  ];
}
