import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GraphGenerator } from './graph-generator/graph-generator';
import { TextFromDataset } from './text-from-dataset/text-from-dataset';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, GraphGenerator, TextFromDataset],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('graph-app-frontend');
}
