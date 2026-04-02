import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextFromDataset } from './text-from-dataset';

describe('TextFromDataset', () => {
  let component: TextFromDataset;
  let fixture: ComponentFixture<TextFromDataset>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TextFromDataset]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TextFromDataset);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
