import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransformedGraphs } from './transformed-graphs';

describe('TransformedGraphs', () => {
  let component: TransformedGraphs;
  let fixture: ComponentFixture<TransformedGraphs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TransformedGraphs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TransformedGraphs);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
