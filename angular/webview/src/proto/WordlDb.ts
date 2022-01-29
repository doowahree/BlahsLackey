/* eslint-disable */
import { util, configure, Writer, Reader } from "protobufjs/minimal";
import * as Long from "long";

export const protobufPackage = "";

export interface GameRecord {
  game: string;
  attempts: number;
  maxAttempts: number;
  extraData: string;
}

export interface UserRecord {
  lastKnownName: string;
  classicGames: { [key: string]: GameRecord };
  customGames: { [key: string]: GameRecord };
}

export interface UserRecord_ClassicGamesEntry {
  key: string;
  value: GameRecord | undefined;
}

export interface UserRecord_CustomGamesEntry {
  key: string;
  value: GameRecord | undefined;
}

export interface WordleSeason {
  name: string;
  filename: string;
  users: { [key: string]: UserRecord };
}

export interface WordleSeason_UsersEntry {
  key: string;
  value: UserRecord | undefined;
}

export interface WordlSeasonFileDb {
  currentFile: string;
  currentSeasonName: string;
  filenameToSeasonName: { [key: string]: string };
}

export interface WordlSeasonFileDb_FilenameToSeasonNameEntry {
  key: string;
  value: string;
}

function createBaseGameRecord(): GameRecord {
  return { game: "", attempts: 0, maxAttempts: 0, extraData: "" };
}

export const GameRecord = {
  encode(message: GameRecord, writer: Writer = Writer.create()): Writer {
    if (message.game !== "") {
      writer.uint32(10).string(message.game);
    }
    if (message.attempts !== 0) {
      writer.uint32(16).int32(message.attempts);
    }
    if (message.maxAttempts !== 0) {
      writer.uint32(24).int32(message.maxAttempts);
    }
    if (message.extraData !== "") {
      writer.uint32(34).string(message.extraData);
    }
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): GameRecord {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGameRecord();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.game = reader.string();
          break;
        case 2:
          message.attempts = reader.int32();
          break;
        case 3:
          message.maxAttempts = reader.int32();
          break;
        case 4:
          message.extraData = reader.string();
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): GameRecord {
    return {
      game: isSet(object.game) ? String(object.game) : "",
      attempts: isSet(object.attempts) ? Number(object.attempts) : 0,
      maxAttempts: isSet(object.maxAttempts) ? Number(object.maxAttempts) : 0,
      extraData: isSet(object.extraData) ? String(object.extraData) : "",
    };
  },

  toJSON(message: GameRecord): unknown {
    const obj: any = {};
    message.game !== undefined && (obj.game = message.game);
    message.attempts !== undefined &&
      (obj.attempts = Math.round(message.attempts));
    message.maxAttempts !== undefined &&
      (obj.maxAttempts = Math.round(message.maxAttempts));
    message.extraData !== undefined && (obj.extraData = message.extraData);
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<GameRecord>, I>>(
    object: I
  ): GameRecord {
    const message = createBaseGameRecord();
    message.game = object.game ?? "";
    message.attempts = object.attempts ?? 0;
    message.maxAttempts = object.maxAttempts ?? 0;
    message.extraData = object.extraData ?? "";
    return message;
  },
};

function createBaseUserRecord(): UserRecord {
  return { lastKnownName: "", classicGames: {}, customGames: {} };
}

export const UserRecord = {
  encode(message: UserRecord, writer: Writer = Writer.create()): Writer {
    if (message.lastKnownName !== "") {
      writer.uint32(26).string(message.lastKnownName);
    }
    Object.entries(message.classicGames).forEach(([key, value]) => {
      UserRecord_ClassicGamesEntry.encode(
        { key: key as any, value },
        writer.uint32(10).fork()
      ).ldelim();
    });
    Object.entries(message.customGames).forEach(([key, value]) => {
      UserRecord_CustomGamesEntry.encode(
        { key: key as any, value },
        writer.uint32(18).fork()
      ).ldelim();
    });
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): UserRecord {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseUserRecord();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 3:
          message.lastKnownName = reader.string();
          break;
        case 1:
          const entry1 = UserRecord_ClassicGamesEntry.decode(
            reader,
            reader.uint32()
          );
          if (entry1.value !== undefined) {
            message.classicGames[entry1.key] = entry1.value;
          }
          break;
        case 2:
          const entry2 = UserRecord_CustomGamesEntry.decode(
            reader,
            reader.uint32()
          );
          if (entry2.value !== undefined) {
            message.customGames[entry2.key] = entry2.value;
          }
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): UserRecord {
    return {
      lastKnownName: isSet(object.lastKnownName)
        ? String(object.lastKnownName)
        : "",
      classicGames: isObject(object.classicGames)
        ? Object.entries(object.classicGames).reduce<{
            [key: string]: GameRecord;
          }>((acc, [key, value]) => {
            acc[key] = GameRecord.fromJSON(value);
            return acc;
          }, {})
        : {},
      customGames: isObject(object.customGames)
        ? Object.entries(object.customGames).reduce<{
            [key: string]: GameRecord;
          }>((acc, [key, value]) => {
            acc[key] = GameRecord.fromJSON(value);
            return acc;
          }, {})
        : {},
    };
  },

  toJSON(message: UserRecord): unknown {
    const obj: any = {};
    message.lastKnownName !== undefined &&
      (obj.lastKnownName = message.lastKnownName);
    obj.classicGames = {};
    if (message.classicGames) {
      Object.entries(message.classicGames).forEach(([k, v]) => {
        obj.classicGames[k] = GameRecord.toJSON(v);
      });
    }
    obj.customGames = {};
    if (message.customGames) {
      Object.entries(message.customGames).forEach(([k, v]) => {
        obj.customGames[k] = GameRecord.toJSON(v);
      });
    }
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<UserRecord>, I>>(
    object: I
  ): UserRecord {
    const message = createBaseUserRecord();
    message.lastKnownName = object.lastKnownName ?? "";
    message.classicGames = Object.entries(object.classicGames ?? {}).reduce<{
      [key: string]: GameRecord;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = GameRecord.fromPartial(value);
      }
      return acc;
    }, {});
    message.customGames = Object.entries(object.customGames ?? {}).reduce<{
      [key: string]: GameRecord;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = GameRecord.fromPartial(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseUserRecord_ClassicGamesEntry(): UserRecord_ClassicGamesEntry {
  return { key: "", value: undefined };
}

export const UserRecord_ClassicGamesEntry = {
  encode(
    message: UserRecord_ClassicGamesEntry,
    writer: Writer = Writer.create()
  ): Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== undefined) {
      GameRecord.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(
    input: Reader | Uint8Array,
    length?: number
  ): UserRecord_ClassicGamesEntry {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseUserRecord_ClassicGamesEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.key = reader.string();
          break;
        case 2:
          message.value = GameRecord.decode(reader, reader.uint32());
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): UserRecord_ClassicGamesEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value)
        ? GameRecord.fromJSON(object.value)
        : undefined,
    };
  },

  toJSON(message: UserRecord_ClassicGamesEntry): unknown {
    const obj: any = {};
    message.key !== undefined && (obj.key = message.key);
    message.value !== undefined &&
      (obj.value = message.value
        ? GameRecord.toJSON(message.value)
        : undefined);
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<UserRecord_ClassicGamesEntry>, I>>(
    object: I
  ): UserRecord_ClassicGamesEntry {
    const message = createBaseUserRecord_ClassicGamesEntry();
    message.key = object.key ?? "";
    message.value =
      object.value !== undefined && object.value !== null
        ? GameRecord.fromPartial(object.value)
        : undefined;
    return message;
  },
};

function createBaseUserRecord_CustomGamesEntry(): UserRecord_CustomGamesEntry {
  return { key: "", value: undefined };
}

export const UserRecord_CustomGamesEntry = {
  encode(
    message: UserRecord_CustomGamesEntry,
    writer: Writer = Writer.create()
  ): Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== undefined) {
      GameRecord.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(
    input: Reader | Uint8Array,
    length?: number
  ): UserRecord_CustomGamesEntry {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseUserRecord_CustomGamesEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.key = reader.string();
          break;
        case 2:
          message.value = GameRecord.decode(reader, reader.uint32());
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): UserRecord_CustomGamesEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value)
        ? GameRecord.fromJSON(object.value)
        : undefined,
    };
  },

  toJSON(message: UserRecord_CustomGamesEntry): unknown {
    const obj: any = {};
    message.key !== undefined && (obj.key = message.key);
    message.value !== undefined &&
      (obj.value = message.value
        ? GameRecord.toJSON(message.value)
        : undefined);
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<UserRecord_CustomGamesEntry>, I>>(
    object: I
  ): UserRecord_CustomGamesEntry {
    const message = createBaseUserRecord_CustomGamesEntry();
    message.key = object.key ?? "";
    message.value =
      object.value !== undefined && object.value !== null
        ? GameRecord.fromPartial(object.value)
        : undefined;
    return message;
  },
};

function createBaseWordleSeason(): WordleSeason {
  return { name: "", filename: "", users: {} };
}

export const WordleSeason = {
  encode(message: WordleSeason, writer: Writer = Writer.create()): Writer {
    if (message.name !== "") {
      writer.uint32(10).string(message.name);
    }
    if (message.filename !== "") {
      writer.uint32(18).string(message.filename);
    }
    Object.entries(message.users).forEach(([key, value]) => {
      WordleSeason_UsersEntry.encode(
        { key: key as any, value },
        writer.uint32(26).fork()
      ).ldelim();
    });
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): WordleSeason {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseWordleSeason();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.name = reader.string();
          break;
        case 2:
          message.filename = reader.string();
          break;
        case 3:
          const entry3 = WordleSeason_UsersEntry.decode(
            reader,
            reader.uint32()
          );
          if (entry3.value !== undefined) {
            message.users[entry3.key] = entry3.value;
          }
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): WordleSeason {
    return {
      name: isSet(object.name) ? String(object.name) : "",
      filename: isSet(object.filename) ? String(object.filename) : "",
      users: isObject(object.users)
        ? Object.entries(object.users).reduce<{ [key: string]: UserRecord }>(
            (acc, [key, value]) => {
              acc[key] = UserRecord.fromJSON(value);
              return acc;
            },
            {}
          )
        : {},
    };
  },

  toJSON(message: WordleSeason): unknown {
    const obj: any = {};
    message.name !== undefined && (obj.name = message.name);
    message.filename !== undefined && (obj.filename = message.filename);
    obj.users = {};
    if (message.users) {
      Object.entries(message.users).forEach(([k, v]) => {
        obj.users[k] = UserRecord.toJSON(v);
      });
    }
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<WordleSeason>, I>>(
    object: I
  ): WordleSeason {
    const message = createBaseWordleSeason();
    message.name = object.name ?? "";
    message.filename = object.filename ?? "";
    message.users = Object.entries(object.users ?? {}).reduce<{
      [key: string]: UserRecord;
    }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = UserRecord.fromPartial(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseWordleSeason_UsersEntry(): WordleSeason_UsersEntry {
  return { key: "", value: undefined };
}

export const WordleSeason_UsersEntry = {
  encode(
    message: WordleSeason_UsersEntry,
    writer: Writer = Writer.create()
  ): Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== undefined) {
      UserRecord.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): WordleSeason_UsersEntry {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseWordleSeason_UsersEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.key = reader.string();
          break;
        case 2:
          message.value = UserRecord.decode(reader, reader.uint32());
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): WordleSeason_UsersEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value)
        ? UserRecord.fromJSON(object.value)
        : undefined,
    };
  },

  toJSON(message: WordleSeason_UsersEntry): unknown {
    const obj: any = {};
    message.key !== undefined && (obj.key = message.key);
    message.value !== undefined &&
      (obj.value = message.value
        ? UserRecord.toJSON(message.value)
        : undefined);
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<WordleSeason_UsersEntry>, I>>(
    object: I
  ): WordleSeason_UsersEntry {
    const message = createBaseWordleSeason_UsersEntry();
    message.key = object.key ?? "";
    message.value =
      object.value !== undefined && object.value !== null
        ? UserRecord.fromPartial(object.value)
        : undefined;
    return message;
  },
};

function createBaseWordlSeasonFileDb(): WordlSeasonFileDb {
  return { currentFile: "", currentSeasonName: "", filenameToSeasonName: {} };
}

export const WordlSeasonFileDb = {
  encode(message: WordlSeasonFileDb, writer: Writer = Writer.create()): Writer {
    if (message.currentFile !== "") {
      writer.uint32(10).string(message.currentFile);
    }
    if (message.currentSeasonName !== "") {
      writer.uint32(18).string(message.currentSeasonName);
    }
    Object.entries(message.filenameToSeasonName).forEach(([key, value]) => {
      WordlSeasonFileDb_FilenameToSeasonNameEntry.encode(
        { key: key as any, value },
        writer.uint32(26).fork()
      ).ldelim();
    });
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): WordlSeasonFileDb {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseWordlSeasonFileDb();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.currentFile = reader.string();
          break;
        case 2:
          message.currentSeasonName = reader.string();
          break;
        case 3:
          const entry3 = WordlSeasonFileDb_FilenameToSeasonNameEntry.decode(
            reader,
            reader.uint32()
          );
          if (entry3.value !== undefined) {
            message.filenameToSeasonName[entry3.key] = entry3.value;
          }
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): WordlSeasonFileDb {
    return {
      currentFile: isSet(object.currentFile) ? String(object.currentFile) : "",
      currentSeasonName: isSet(object.currentSeasonName)
        ? String(object.currentSeasonName)
        : "",
      filenameToSeasonName: isObject(object.filenameToSeasonName)
        ? Object.entries(object.filenameToSeasonName).reduce<{
            [key: string]: string;
          }>((acc, [key, value]) => {
            acc[key] = String(value);
            return acc;
          }, {})
        : {},
    };
  },

  toJSON(message: WordlSeasonFileDb): unknown {
    const obj: any = {};
    message.currentFile !== undefined &&
      (obj.currentFile = message.currentFile);
    message.currentSeasonName !== undefined &&
      (obj.currentSeasonName = message.currentSeasonName);
    obj.filenameToSeasonName = {};
    if (message.filenameToSeasonName) {
      Object.entries(message.filenameToSeasonName).forEach(([k, v]) => {
        obj.filenameToSeasonName[k] = v;
      });
    }
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<WordlSeasonFileDb>, I>>(
    object: I
  ): WordlSeasonFileDb {
    const message = createBaseWordlSeasonFileDb();
    message.currentFile = object.currentFile ?? "";
    message.currentSeasonName = object.currentSeasonName ?? "";
    message.filenameToSeasonName = Object.entries(
      object.filenameToSeasonName ?? {}
    ).reduce<{ [key: string]: string }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = String(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseWordlSeasonFileDb_FilenameToSeasonNameEntry(): WordlSeasonFileDb_FilenameToSeasonNameEntry {
  return { key: "", value: "" };
}

export const WordlSeasonFileDb_FilenameToSeasonNameEntry = {
  encode(
    message: WordlSeasonFileDb_FilenameToSeasonNameEntry,
    writer: Writer = Writer.create()
  ): Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== "") {
      writer.uint32(18).string(message.value);
    }
    return writer;
  },

  decode(
    input: Reader | Uint8Array,
    length?: number
  ): WordlSeasonFileDb_FilenameToSeasonNameEntry {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseWordlSeasonFileDb_FilenameToSeasonNameEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.key = reader.string();
          break;
        case 2:
          message.value = reader.string();
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): WordlSeasonFileDb_FilenameToSeasonNameEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value) ? String(object.value) : "",
    };
  },

  toJSON(message: WordlSeasonFileDb_FilenameToSeasonNameEntry): unknown {
    const obj: any = {};
    message.key !== undefined && (obj.key = message.key);
    message.value !== undefined && (obj.value = message.value);
    return obj;
  },

  fromPartial<
    I extends Exact<DeepPartial<WordlSeasonFileDb_FilenameToSeasonNameEntry>, I>
  >(object: I): WordlSeasonFileDb_FilenameToSeasonNameEntry {
    const message = createBaseWordlSeasonFileDb_FilenameToSeasonNameEntry();
    message.key = object.key ?? "";
    message.value = object.value ?? "";
    return message;
  },
};

type Builtin =
  | Date
  | Function
  | Uint8Array
  | string
  | number
  | boolean
  | undefined;

export type DeepPartial<T> = T extends Builtin
  ? T
  : T extends Array<infer U>
  ? Array<DeepPartial<U>>
  : T extends ReadonlyArray<infer U>
  ? ReadonlyArray<DeepPartial<U>>
  : T extends {}
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
export type Exact<P, I extends P> = P extends Builtin
  ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & Record<
        Exclude<keyof I, KeysOfUnion<P>>,
        never
      >;

// If you get a compile-error about 'Constructor<Long> and ... have no overlap',
// add '--ts_proto_opt=esModuleInterop=true' as a flag when calling 'protoc'.
if (util.Long !== Long) {
  util.Long = Long as any;
  configure();
}

function isObject(value: any): boolean {
  return typeof value === "object" && value !== null;
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
