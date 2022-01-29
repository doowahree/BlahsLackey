/* eslint-disable */
import { util, configure, Writer, Reader } from "protobufjs/minimal";
import * as Long from "long";

export const protobufPackage = "";

export interface AvailableListeners {
  listeners: string[];
}

export interface ListenerMapping {
  channelToListenerMapping: { [key: string]: AvailableListeners };
}

export interface ListenerMapping_ChannelToListenerMappingEntry {
  key: string;
  value: AvailableListeners | undefined;
}

function createBaseAvailableListeners(): AvailableListeners {
  return { listeners: [] };
}

export const AvailableListeners = {
  encode(
    message: AvailableListeners,
    writer: Writer = Writer.create()
  ): Writer {
    for (const v of message.listeners) {
      writer.uint32(10).string(v!);
    }
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): AvailableListeners {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseAvailableListeners();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.listeners.push(reader.string());
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): AvailableListeners {
    return {
      listeners: Array.isArray(object?.listeners)
        ? object.listeners.map((e: any) => String(e))
        : [],
    };
  },

  toJSON(message: AvailableListeners): unknown {
    const obj: any = {};
    if (message.listeners) {
      obj.listeners = message.listeners.map((e) => e);
    } else {
      obj.listeners = [];
    }
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<AvailableListeners>, I>>(
    object: I
  ): AvailableListeners {
    const message = createBaseAvailableListeners();
    message.listeners = object.listeners?.map((e) => e) || [];
    return message;
  },
};

function createBaseListenerMapping(): ListenerMapping {
  return { channelToListenerMapping: {} };
}

export const ListenerMapping = {
  encode(message: ListenerMapping, writer: Writer = Writer.create()): Writer {
    Object.entries(message.channelToListenerMapping).forEach(([key, value]) => {
      ListenerMapping_ChannelToListenerMappingEntry.encode(
        { key: key as any, value },
        writer.uint32(10).fork()
      ).ldelim();
    });
    return writer;
  },

  decode(input: Reader | Uint8Array, length?: number): ListenerMapping {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseListenerMapping();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          const entry1 = ListenerMapping_ChannelToListenerMappingEntry.decode(
            reader,
            reader.uint32()
          );
          if (entry1.value !== undefined) {
            message.channelToListenerMapping[entry1.key] = entry1.value;
          }
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): ListenerMapping {
    return {
      channelToListenerMapping: isObject(object.channelToListenerMapping)
        ? Object.entries(object.channelToListenerMapping).reduce<{
            [key: string]: AvailableListeners;
          }>((acc, [key, value]) => {
            acc[key] = AvailableListeners.fromJSON(value);
            return acc;
          }, {})
        : {},
    };
  },

  toJSON(message: ListenerMapping): unknown {
    const obj: any = {};
    obj.channelToListenerMapping = {};
    if (message.channelToListenerMapping) {
      Object.entries(message.channelToListenerMapping).forEach(([k, v]) => {
        obj.channelToListenerMapping[k] = AvailableListeners.toJSON(v);
      });
    }
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<ListenerMapping>, I>>(
    object: I
  ): ListenerMapping {
    const message = createBaseListenerMapping();
    message.channelToListenerMapping = Object.entries(
      object.channelToListenerMapping ?? {}
    ).reduce<{ [key: string]: AvailableListeners }>((acc, [key, value]) => {
      if (value !== undefined) {
        acc[key] = AvailableListeners.fromPartial(value);
      }
      return acc;
    }, {});
    return message;
  },
};

function createBaseListenerMapping_ChannelToListenerMappingEntry(): ListenerMapping_ChannelToListenerMappingEntry {
  return { key: "", value: undefined };
}

export const ListenerMapping_ChannelToListenerMappingEntry = {
  encode(
    message: ListenerMapping_ChannelToListenerMappingEntry,
    writer: Writer = Writer.create()
  ): Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== undefined) {
      AvailableListeners.encode(
        message.value,
        writer.uint32(18).fork()
      ).ldelim();
    }
    return writer;
  },

  decode(
    input: Reader | Uint8Array,
    length?: number
  ): ListenerMapping_ChannelToListenerMappingEntry {
    const reader = input instanceof Reader ? input : new Reader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseListenerMapping_ChannelToListenerMappingEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.key = reader.string();
          break;
        case 2:
          message.value = AvailableListeners.decode(reader, reader.uint32());
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  },

  fromJSON(object: any): ListenerMapping_ChannelToListenerMappingEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value)
        ? AvailableListeners.fromJSON(object.value)
        : undefined,
    };
  },

  toJSON(message: ListenerMapping_ChannelToListenerMappingEntry): unknown {
    const obj: any = {};
    message.key !== undefined && (obj.key = message.key);
    message.value !== undefined &&
      (obj.value = message.value
        ? AvailableListeners.toJSON(message.value)
        : undefined);
    return obj;
  },

  fromPartial<
    I extends Exact<
      DeepPartial<ListenerMapping_ChannelToListenerMappingEntry>,
      I
    >
  >(object: I): ListenerMapping_ChannelToListenerMappingEntry {
    const message = createBaseListenerMapping_ChannelToListenerMappingEntry();
    message.key = object.key ?? "";
    message.value =
      object.value !== undefined && object.value !== null
        ? AvailableListeners.fromPartial(object.value)
        : undefined;
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
