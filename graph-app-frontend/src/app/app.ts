import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GraphGenerator } from './graph-generator/graph-generator';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, GraphGenerator],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('graph-app-frontend');
}
