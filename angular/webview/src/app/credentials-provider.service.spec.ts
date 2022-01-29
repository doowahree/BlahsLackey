import { TestBed } from '@angular/core/testing';

import { CredentialsProviderService } from './credentials-provider.service';

describe('CredentialsProviderService', () => {
  let service: CredentialsProviderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CredentialsProviderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
