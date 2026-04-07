import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DataService } from '../service/data.service';
import { API_ENDPOINTS } from '../service/api-endpoints';

@Component({
  selector: 'text-from-dataset',
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  templateUrl: './text-from-dataset.html',
  styleUrl: './text-from-dataset.scss',
})
export class TextFromDataset {
  private dataService = inject(DataService);
  text = signal<string | null>(null);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);

  getText() {
      this.isLoading.set(true);
      this.errorMessage.set(null);
      this.text.set(null);

      this.dataService.sendGetRequest<{text: string}>(`${API_ENDPOINTS.RANDOM_TEXT}`).subscribe({
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
