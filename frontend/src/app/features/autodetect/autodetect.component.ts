import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { AutodetectService } from '../../core/services/autodetect.service';

@Component({
  selector: 'app-autodetect',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './autodetect.component.html',
  styleUrls: ['./autodetect.component.scss']
})
export class AutodetectComponent {
  archivosMuestra: File[] = [];
  camposDetectados: any[] = [];
  estadisticas: any = null;
  cargando = false;
  error: string | null = null;

  constructor(private autodetectService: AutodetectService) {}

  onFilesSelected(event: any): void {
    const files = event.target.files;
    this.archivosMuestra = Array.from(files);
  }

  analizarArchivos(): void {
    if (this.archivosMuestra.length === 0) {
      this.error = 'Por favor selecciona al menos un archivo';
      return;
    }

    this.cargando = true;
    this.error = null;

    const fileList = this.createFileList(this.archivosMuestra);

    this.autodetectService.analyzeFiles(fileList).subscribe({
      next: (result) => {
        this.camposDetectados = result.detected_fields;
        this.estadisticas = result.statistics;
        this.cargando = false;
      },
      error: (err) => {
        this.error = 'Error al analizar archivos: ' + err.message;
        this.cargando = false;
      }
    });
  }

  private createFileList(files: File[]): FileList {
    const dataTransfer = new DataTransfer();
    files.forEach(file => dataTransfer.items.add(file));
    return dataTransfer.files;
  }
}
