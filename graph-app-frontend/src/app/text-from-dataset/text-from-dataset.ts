import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { DataService } from '../service/data.service';
import { API_ENDPOINTS } from '../service/api-endpoints';
import { DATASETS_PATH } from '../service/datasets';

@Component({
  selector: 'text-from-dataset',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatSelectModule, MatFormFieldModule],  templateUrl: './text-from-dataset.html',
  styleUrl: './text-from-dataset.scss',
})
export class TextFromDataset {
  private dataService = inject(DataService);
  text = signal<string | null>(null);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  protected readonly DATASETS_PATH = DATASETS_PATH;
  selectedDataset = signal<string>(DATASETS_PATH.SCIERC);

  getText() {
      this.isLoading.set(true);
      this.errorMessage.set(null);
      this.text.set(null);

      this.dataService.sendGetRequest<{text: string}>(`${API_ENDPOINTS.RANDOM_TEXT}?file_path=${this.selectedDataset()}`).subscribe({
        next: (response) => {
          this.text.set(response.text);
          this.dataService.textFromDataset.set(response.text);
          this.isLoading.set(false);
        },
        error: (err) => {
          console.error('Error:', err);
          this.errorMessage.set('An error occurred while fetching the text.');
          this.isLoading.set(false);
        }
      });
    }
}
