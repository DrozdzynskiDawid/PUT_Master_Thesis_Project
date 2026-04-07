import { CommonModule } from '@angular/common';
import { Component, signal, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { DataService } from '../service/data.service';
import { API_ENDPOINTS } from '../service/api-endpoints';

@Component({
  selector: 'transformed-graphs',
  imports: [CommonModule, MatButtonModule],
  templateUrl: './transformed-graphs.html',
  styleUrl: './transformed-graphs.scss',
  standalone: true,
})
export class TransformedGraphs {
  private dataService = inject(DataService);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  graphXGIImageUrl = signal<string | null>(null);
  graphLLMImageUrl = signal<string | null>(null);

  fetchData() {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    if (this.graphXGIImageUrl()) {
      URL.revokeObjectURL(this.graphXGIImageUrl()!);
      this.graphXGIImageUrl.set(null);
    }
    if (this.graphLLMImageUrl()) {
      URL.revokeObjectURL(this.graphLLMImageUrl()!);
      this.graphLLMImageUrl.set(null);
    }
    
    this.dataService.sendPostRequestJson<any>(`${API_ENDPOINTS.TRANSFORM_CLIQUE}`, this.dataService.hypergraphJsonData()).subscribe({
      next: (response) => {
        this.generateGraphImageFromData(response, false);
        console.log('JSON graph data:', response);
      },
      error: (err) => {
        console.error('Error:', err);
        this.errorMessage.set('Error occurred while fetching graph data.');
        this.isLoading.set(false);
      }
    });

    this.dataService.sendPostRequestJson<any>(`${API_ENDPOINTS.TRANSFORM_LLM}`, this.dataService.hypergraphJsonData()).subscribe({
      next: (response) => {
        this.generateGraphImageFromData(response, true);
        console.log('JSON graph data:', response);
      },
      error: (err) => {
        console.error('Error:', err);
        this.errorMessage.set('Error occurred while fetching graph data.');
        this.isLoading.set(false);
      }
    });
  }

  private generateGraphImageFromData(graphData: any, isLLM: boolean = false) {
    this.dataService.sendPostRequestBlob(`${API_ENDPOINTS.GRAPH_PNG}`, graphData).subscribe({
      next: (imageBlob: Blob) => {
        const url = URL.createObjectURL(imageBlob);
        if (isLLM) {
          this.graphLLMImageUrl.set(url);
        } else {
          this.graphXGIImageUrl.set(url);
        }
        this.isLoading.set(false); 
      },
      error: (err) => {
        console.error('Error generating image:', err);
        this.errorMessage.set('An error occurred while generating the graph image from JSON data.');
        this.isLoading.set(false);
      }
    });
  }
}
