import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphGenerator } from './graph-generator';

describe('GraphGenerator', () => {
  let component: GraphGenerator;
  let fixture: ComponentFixture<GraphGenerator>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GraphGenerator]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GraphGenerator);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
