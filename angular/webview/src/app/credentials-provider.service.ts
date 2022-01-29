import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

interface UserToken {
  access_token: string;
  expire_in: number;
  refresh_token: string;
  scope: string;
  token_type: string;
  user: {
    id: number;
    username: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class CredentialsProviderService {


  public credentialReady: EventEmitter<boolean> = new EventEmitter<boolean>();
  private userToken: UserToken | null = null;

  constructor(private http: HttpClient) {
    let discord_data = window.localStorage.getItem('discord_data');
    if (discord_data) {
      this.userToken = JSON.parse(discord_data);
    }
  }

  public isIdentified(): boolean {
    return this.userToken != null
  }

  public identifyWithDiscordCredentials(token: string) {
    this.http.get<UserToken>(`/identify/${window.location.protocol}/${window.location.host}/${token}`).subscribe((data: UserToken) => {
      document.cookie = `discord_access_token=${data.access_token}`;
      document.cookie = `discord_refresh_token=${data.refresh_token}`;
      document.cookie = `discord_user_id=${data.user.id}`;
      document.cookie = `discord_user_name=${data.user.username}`;
      window.localStorage.setItem('discord_data', JSON.stringify(data));
      this.userToken = data;
      window.location.reload();
    })
  }

  public getUserToken(): UserToken | null{

    return this.userToken;
  }


}
