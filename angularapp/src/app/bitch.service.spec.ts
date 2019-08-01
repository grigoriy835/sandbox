import { TestBed } from '@angular/core/testing';

import { BitchService } from './bitch.service';

describe('BitchService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BitchService = TestBed.get(BitchService);
    expect(service).toBeTruthy();
  });
});
