import argparse
import logging
from subtitle.type import WhisperModelEnum
from subtitle.action import Action


# 命令行参数解析
def getParser():
    parser = argparse.ArgumentParser(
        description="Generate subtitles of video by whisper transcribe",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("inputs", type=str, nargs="+", help="Inputs filenames/folders")
    parser.add_argument(
        "-t",
        "--transcribe",
        help="Transcribe videos/audio into subtitles",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-tl",
        "--translate",
        help="1.Transcribe videos/audio to subtitles. 2.Translate generated subtitles to target language",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-a",
        "--add",
        help="Add generated subtitles into video",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-u",
        "--union",
        help="Union operations,including transcribe->translate->add subtitles to video",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-ut",
        "--union-transcribe",
        help="Union operations,including transcribe->add subtitles to video,not including translate",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--outputs", type=str, nargs="+", help="Outputs filenames/folders"
    )
    parser.add_argument(
        "--target-subtitles",
        nargs="+",
        default=None,
        help="The file name of target subtitles,if it's not specified,generate subtiltles for input",
    )
    parser.add_argument(
        "--China",
        default=None,
        help="Google translate is disable,cannot translate subtitles",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="The directory of output,default is current path",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        choices=[
            "zh",
            "en",
            "Afrikaans",
            "Arabic",
            "Armenian",
            "Azerbaijani",
            "Belarusian",
            "Bosnian",
            "Bulgarian",
            "Catalan",
            "Croatian",
            "Czech",
            "Danish",
            "Dutch",
            "Estonian",
            "Finnish",
            "French",
            "Galician",
            "German",
            "Greek",
            "Hebrew",
            "Hindi",
            "Hungarian",
            "Icelandic",
            "Indonesian",
            "Italian",
            "Japanese",
            "Kannada",
            "Kazakh",
            "Korean",
            "Latvian",
            "Lithuanian",
            "Macedonian",
            "Malay",
            "Marathi",
            "Maori",
            "Nepali",
            "Norwegian",
            "Persian",
            "Polish",
            "Portuguese",
            "Romanian",
            "Russian",
            "Serbian",
            "Slovak",
            "Slovenian",
            "Spanish",
            "Swahili",
            "Swedish",
            "Tagalog",
            "Tamil",
            "Thai",
            "Turkish",
            "Ukrainian",
            "Urdu",
            "Vietnamese",
            "Welsh",
        ],
        help="The input language of transcription/translation",
    )
    parser.add_argument(
        "--target-lang",
        type=str,
        default="zh",
        choices=[
            "zh",
            "en",
            "Afrikaans",
            "Arabic",
            "Armenian",
            "Azerbaijani",
            "Belarusian",
            "Bosnian",
            "Bulgarian",
            "Catalan",
            "Croatian",
            "Czech",
            "Danish",
            "Dutch",
            "Estonian",
            "Finnish",
            "French",
            "Galician",
            "German",
            "Greek",
            "Hebrew",
            "Hindi",
            "Hungarian",
            "Icelandic",
            "Indonesian",
            "Italian",
            "Japanese",
            "Kannada",
            "Kazakh",
            "Korean",
            "Latvian",
            "Lithuanian",
            "Macedonian",
            "Malay",
            "Marathi",
            "Maori",
            "Nepali",
            "Norwegian",
            "Persian",
            "Polish",
            "Portuguese",
            "Romanian",
            "Russian",
            "Serbian",
            "Slovak",
            "Slovenian",
            "Spanish",
            "Swahili",
            "Swedish",
            "Tagalog",
            "Tamil",
            "Thai",
            "Turkish",
            "Ukrainian",
            "Urdu",
            "Vietnamese",
            "Welsh",
        ],
        help="The output language of translation",
    )
    parser.add_argument(
        "--whisper-model",
        type=str,
        default=WhisperModelEnum.SMALL.value,
        choices=WhisperModelEnum.get_values(),
        help="The whisper model used to transcribe.",
    )
    parser.add_argument(
        "--bitrate",
        type=str,
        default="10m",
        help="The bitrate to export the cutted video, such as 10m, 1m, or 500k",
    )
    # whisper 不支持mps
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Force to CPU/GPU for transcribing. In default automatically use GPU if available.",
    )

    return parser


def main():
    # 命令行参数
    parser = getParser()
    logging.basicConfig(
        format="[parrot:%(filename)s:L%(lineno)d] %(levelname)-6s %(message)s"
    )
    logging.getLogger().setLevel(logging.INFO)
    args = parser.parse_args()
    print(args)
    if args.transcribe:
        logging.info("Transcribe start")

        Action(args).transcribe()
    elif args.translate:
        logging.info(f"Translate starting,input file->{args.inputs}")
        Action(args).translate()

    elif args.add:
        logging.info(
            f"Add subtitle->[{args.target_subtitles}] for [{args.inputs}] start"
        )
        Action(args).add_subtitles()

    elif args.union:
        logging.info(f"Union operations for [{args.inputs}] start")
        Action(args).union()
    elif args.union_transcribe:
        logging.info(
            f"Union operations not including translate for [{args.inputs}] start"
        )
        Action(args).unionForTranscribe()


#
if __name__ == "__main__":
    main()
