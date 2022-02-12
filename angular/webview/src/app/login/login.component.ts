import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {CredentialsProviderService} from "../credentials-provider.service";
import {Observable, Subject} from "rxjs";
import {HttpClient} from "@angular/common/http";

interface ClientIdResponse {
  client_id: string;
  is_dev: boolean;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  public isLoggedIn: boolean = false;
  public username: string = '';
  public readyToIdentify: boolean = false;
  public clientId: string = '';
  public clientIdObservable = new Subject<string>();
  public counter: number = 0;

  constructor(private readonly credentials: CredentialsProviderService, private readonly http: HttpClient, private changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    if (location.host.includes('.com') && location.protocol === 'http:') {
       window.location.href = location.href.replace('http', 'https');
    }

    if (this.credentials.isIdentified()) {
      this.isLoggedIn = true;
      this.username = this.credentials.getUserToken()?.user.username || 'N/A';
    } else {
      let sp = new URLSearchParams(window.location.search);
      let code = sp.get('code')
      if (code) {
        this.credentials.identifyWithDiscordCredentials(code);
      } else {
        this.http.get<ClientIdResponse>(this.credentials.makeApiUrls('/api/identify_client_id')).subscribe(this._bindClientId.bind(this));
        console.log(this);
      }
    }
  }

  _bindClientId(data: ClientIdResponse) {
    this.counter++;
    this.readyToIdentify = true;
    this.clientId = data.client_id;

    this.clientIdObservable.next(this.clientId);
    // this.changeDetectorRef.detectChanges();
    console.log(data.client_id, ' with change detection');
  }

  login() {
    const url = new URL('https://discord.com/api/oauth2/authorize?response_type=code&scope=identify');
    const params = new URLSearchParams(url.search);

    params.set('redirect_uri', encodeURI(`${location.protocol}//${location.host}`));
    params.set('client_id', this.clientId);
    window.location.href = `https://${url.hostname}${url.pathname}?${params}`;
  }

  test() {
    this.counter++;
  }
}
