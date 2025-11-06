import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BatchService } from '../../core/services/batch.service';

@Component({
  selector: 'app-batch',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './batch.component.html',
  styleUrls: ['./batch.component.scss']
})
export class BatchComponent {
  config = {
    profile_name: '',
    csv_path: '',
    output_folder: '',
    file_prefix: 'procesado'
  };

  generatedScript: string | null = null;
  scriptFilename: string | null = null;
  loading = false;
  error: string | null = null;

  constructor(private batchService: BatchService) {}

  generateScript(): void {
    this.loading = true;
    this.error = null;

    this.batchService.generateScript(this.config).subscribe({
      next: (response) => {
        this.generatedScript = response.script;
        this.scriptFilename = response.filename;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al generar script: ' + err.message;
        this.loading = false;
      }
    });
  }

  downloadScript(): void {
    if (this.generatedScript && this.scriptFilename) {
      this.batchService.downloadScript(this.generatedScript, this.scriptFilename);
    }
  }

  copyToClipboard(): void {
    if (this.generatedScript) {
      navigator.clipboard.writeText(this.generatedScript);
      alert('Script copiado al portapapeles');
    }
  }
}
